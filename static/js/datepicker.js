/* global $ */

$(document).ready(function() {
    $('.datepicker').pickadate({
          selectMonths: true,
          selectYears: 200,
          format: 'd/m/yyyy',
          formatSubmit: 'd/m/yyyy',
          hiddenName: true,
          min: new Date(1910,1,1),
          max: new Date(2030,11,31),
          today: '',
          clear: 'Clear Selection',
    });

 


});

