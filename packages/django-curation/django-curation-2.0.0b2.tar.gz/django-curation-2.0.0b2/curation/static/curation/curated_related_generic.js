/**
 * CURATED RELATED FK
 * generic lookup
 */

(function(){

    var $, jqStr;
    if (typeof window.grp == 'object' && typeof grp.jQuery != 'undefined') {
        $ = grp.jQuery;
        jqStr = 'grp.jQuery';
    } else if (typeof window.django == 'object' && typeof django.jQuery != 'undefined') {
        $ = django.jQuery;
        jqStr = 'django.jQuery';
    } else {
        $ = jQuery;
        jqStr = 'jQuery';
    }

    var lookup_link = function(id, val) {
        if (!window.DJCURATION || !DJCURATION.CONTENT_TYPES) {
            return;
        }
        var ct = DJCURATION.CONTENT_TYPES[val];
        if (!ct) {
            var $content_type = $('#' + id);
            var curationPrefix = $content_type.curationPrefix();
            if (curationPrefix) {
                var inlineRelatedId = curationPrefix.replace(/^id_(.+)\-(\d+)\-$/, '$1$2');
                var inlineRelated = document.getElementById(inlineRelatedId);
                if (inlineRelated) {
                    $(document).trigger('djnesting:lookup', [inlineRelated, {
                        "label": null,
                        "value": null,
                        "fk": {}
                    }]);
                }
            }
            return;
        }

        var $lookuplink = $('<a class="curated-related-lookup"></a>');
        $lookuplink.attr('id', 'lookup_'+id);
        $lookuplink.attr('href', ct.changelist);
        $lookuplink.click(function(evt) {
            return showRelatedObjectLookupPopup(this);
        });

        return $lookuplink;
    };

    var update_lookup = function($content_type, options) {
        var $obj = $content_type.curationFkField();
        if (typeof $obj != 'object' || !$obj.length) {
            return;
        }
        $obj.val('');
        $obj.next().remove();
        $obj.next().remove();
        if ($content_type.val()) {
            var $link = lookup_link($obj.attr('id'), $content_type.val());
            if ($link) {
                $obj.after(options.placeholder).after($link);
            }
        }
    };

    var lookup_id = function($object_id, options) {
        if (!window.DJCURATION || !DJCURATION.CONTENT_TYPES || !DJCURATION.LOOKUP_URL) {
            return;
        }

        var $content_type = $object_id.curationCtField();

        if (typeof($content_type) != 'object' || !$content_type.length) {
            return;
        }

        var $text = $object_id.next().next();
        var ctId = $content_type.val();
        var ct = DJCURATION.CONTENT_TYPES[ctId];
        if (!ct) { return; }

        var curationPrefix = $content_type.curationPrefix();

        var data = $content_type.data();
        $.getJSON(DJCURATION.LOOKUP_URL, {
            object_id: $object_id.val(),
            app_label: ct.app_label,
            model_name: ct.model,
            ct_id: data.contentTypeId,
            ct_field: data.fieldName,
            fk_field: data.fkFieldName
        }, function(data) {
            if (Object.prototype.toString.call(data) == '[object Array]' && data.length == 1) {
                data = data[0];
            }
            var fk;
            if (data.fk) {
                fk = data.fk;
            } else if (data.length && data.length == 1 && typeof data[0] == 'object' && data[0].fk) {
                fk = data[0].fk;
            }

            if (fk) {
                var placeholderFields = $content_type.data('placeholderFields' + ctId) || {};
                for (var fieldName in placeholderFields) {
                    var $input = $('#' + curationPrefix + fieldName);
                    $input.attr('placeholder', '');
                }
                placeholderFields = {};
                for (var fieldName in fk) {
                    var $input = $('#' + curationPrefix + fieldName);
                    if (!$input.length || !$input.is('textarea,input[type="text"]')) {
                        continue;
                    }
                    var val = fk[fieldName];
                    $input.attr('placeholder', val);
                    placeholderFields[fieldName] = val;
                }
                $content_type.data('placeholderFields' + ctId, placeholderFields);
            }

            if (curationPrefix) {
                var inlineRelatedId = curationPrefix.replace(/^id_(.+)\-(\d+)\-$/, '$1$2');
                var inlineRelated = document.getElementById(inlineRelatedId);
                if (inlineRelated) {
                    $(document).trigger('djnesting:lookup', [inlineRelated, data]);
                }
            }

            $text.text(data.label);
        });
    };

    var unbindEvents = function($element) {
        if (typeof($element) != 'object' || !$element.length) {
            return;
        }
        var elementData = $.data($element[0]);
        var internalData = (typeof(elementData) == 'object')
                         ? elementData[$.expando]
                         : null;
        if (typeof internalData != 'object' || !internalData.events) {
            return;
        }
        var events = internalData.events;
        $.each(["change", "focus", "keyup", "blur"], function(n, eventName) {
            if (typeof(events[eventName]) == 'object' && events[eventName].length) {
                for (var i = 0; i < events[eventName].length; i++) {
                    var evt = events[eventName][i];
                    if (typeof(evt.handler) == 'function') {
                        var funcString = evt.handler.toString();
                        if (funcString.match(/lookup_id|update_lookup/)) {
                            $element.unbind(eventName, evt.handler);
                        }
                    }
                }
            }
        });
    };

    var methods = {
        init: function(options) {
            options = $.extend({}, $.fn.curated_related_generic.defaults, options);

            return this.each(function(i, content_type) {
                var $content_type = $(content_type);

                // add placeholder
                var $object_id = $content_type.curationFkField();
                if (typeof $object_id != 'object' || !$object_id.length) {
                    return;
                }

                $object_id.data({
                    'ctFieldName': $content_type.data('fieldName'),
                    'fieldName': $content_type.data('fkFieldName')
                });

                unbindEvents($content_type);
                unbindEvents($object_id);

                $object_id.bind("change focus keyup blur", function() { // id-handler
                    lookup_id($(this), options);
                });
                $content_type.bind("change", function() { // content-type-handler
                    update_lookup($(this), options);
                });

                if ($content_type.val()) {
                    var link = lookup_link($object_id.attr("id"), $content_type.val());
                    if (!link) {
                        return;
                    }
                    $object_id.after(options.placeholder).after(link);
                }
                // lookup
                lookup_id($object_id, options); // lookup when loading page

            });
        }
    };

    $.fn.curated_related_generic = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' +  method + ' does not exist on ' + jqStr + '.curated_related_generic');
        }
        return false;
    };

    $.fn.curated_related_generic.defaults = {
        placeholder: '&nbsp;<span class="curated-related-label"></span>',
        repr_max_length: 30,
        lookup_url: DJCURATION.LOOKUP_URL
    };

    $.fn.old_grp_related_generic = $.fn.grp_related_generic;

    $.fn.grp_related_generic = function() {
        if (typeof $.fn.old_grp_related_generic != 'function') {
            return;
        }

        if ($(this).hasClass('curated-object-id')) {
            return;
        }
        return $.fn.old_grp_related_generic.apply(this, arguments);
    };

})();