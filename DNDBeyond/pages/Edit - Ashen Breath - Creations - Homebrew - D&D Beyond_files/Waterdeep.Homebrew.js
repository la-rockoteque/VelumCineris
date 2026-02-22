(function ($, Cobalt, Waterdeep, undefined) {
    "use strict";
    Waterdeep.Homebrew = {
        toggleIsHomebrewValueBySource: function (realCheckbox, fakeCheckboxContainer, sourceDropdownId, event) {
            if (event.target.id === sourceDropdownId) {
                let hasSourceValue = event.target.selectedOptions[0].value.length > 0
                let isChecked = $(realCheckbox).is(":checked");
                if (hasSourceValue && isChecked) {
                    $(realCheckbox).prop('checked', !isChecked);
                    $(fakeCheckboxContainer).children().first().toggleClass('fc-selected')
                }
            }
        },
    }

})(jQuery, Cobalt, Waterdeep);