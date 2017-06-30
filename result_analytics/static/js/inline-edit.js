
// This stores the serialized initial state of the form in memory.
// In order to tell if the form has changed, we'd serialize it again and
// compare the new state with this.
var formState = null;

$(document).ajaxComplete(function (jqXHR, opts) {
    $('#id_form').ajaxForm({
        success: function(data) {
            $('.form-target').replaceWith(data)
            var $frm = $('.form-target form'),
                scrollTarget;
            if ($frm.size()) {
                initForms($frm)
                scrollTarget = '.form-target'
            } else {
                var $target = $('.add-target, .edit-target')
                scrollTarget = ($target.data('parent-id') ? $target.data('parent-id') : $target)
                if ($target.hasClass('add-target')) {
                    $target.removeClass('add-target')
                    if ($target.data('parent-id')) $target.removeData('parent-id')
                } else {
                    $target.remove()
                }
            }
            $.scrollTo(scrollTarget)
        }
    });
    
    if ($.fn.chainedSelect) $('.chainedSelect').chainedSelect();
    if (typeof initDatepicker !== 'undefined') {
        $('#id_form .vDateField').each(initDatepicker);
    }
    if (typeof initSkillsPicker !== 'undefined') {
        $('#id_form .vSkillsField').each(function(i, o) {
            if (!$(o).data('tokenInputObject')) {
                initSkillsPicker(i, o);
            }
        });
    }
    
    if (typeof window.msnry === 'object') {
        msnry.layout()
    }
});

function removeInlineForm() {
    $('.form-target').hide().remove();
    var $target = $('.add-target, .edit-target').removeClass('add-target edit-target');
    if (typeof window.msnry === 'object') {
        msnry.layout()
    }
    if ($target.size()) {
        if ($target.data('parent-id')) {
            $.scrollTo($target.data('parent-id'))
            $target.removeData('parent-id')
        } else {
            $.scrollTo($target)
        }
    }
}

function showInlineForm(obj, url, editMode) {
    // check if we've got any data in our form; if we do, prompt to save first.
    // TODO: maybe replace the defalt confirm box with something cuter? Very Low Pri.
    // TODO: Fix!!
    /*if (formState != null && $('tr.form-target form').serialize() != formState) {
        if (!confirm("You've made changes to this form. Would you like to discard them?")) {
            return false;
        }
    }*/
    
    removeInlineForm()
    
    var $obj = $(obj)
    $.get(url).done(function(data) {
        var $target;
        if (editMode) {
            $target = $obj.closest('.item, .basicprofile, table').addClass('edit-target')
        } else {
            $target = $obj.closest('.actions').addClass('add-target')
        }
        if ($target.is('TR')) {
            $target.before($('<tr class="form-target"><td colspan="2"></td></tr>'))
        } else {
            $target.before($('<div class="form-target"></div>'))
            $target.data('parent-id', '#' + $obj.parents('.section').prop('id'))
        }
        $('.form-target').replaceWith(data)
        var $frm = $('.form-target form')
        initForms($frm)
        //formState = $frm.serialize()
        if (typeof window.msnry === 'object') {
            msnry.layout()
        }
        $.scrollTo('.form-target')
    })
}

$(function() {
    $('body').on('click', '.add-section, .edit-section', function(evt) {
        evt.preventDefault()
        showInlineForm(this, this.href, $(this).hasClass('edit-section'))
    }).on('click', '.delete-section', function(evt) {
        evt.preventDefault()
        if (confirm("Delete this entry (it'll be gone forever)?")) {
            var $btn = $(this);
            $.ajax({
                url: this.href,
                dataType: 'text',
                type: 'POST',
                success: function(data) {
                    var $$ = $btn.closest('.item, tr');
                    $$.fadeOut(400, function() {
                        $$.remove();
                    });
                }
            });
        }
    }).on('click', '.cancel-btn', removeInlineForm)
});

