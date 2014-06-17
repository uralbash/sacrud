$(function() {
    function move(event, ui) {
      var widget = ui.item.attr('name'),
          column = ui.item.parent().data('number'),
          position = $('.dashboard__column[data-number="'+column+'"]  .widget').index(ui.item),
          data = {'widget': widget, 'column': column, 'position': position};

      $.ajax({
          type: "POST",
          url: 'save_position',
          data: data,
          // success: function(result){},
          error: function (xhr, textStatus, errorThrown) {
              ui.sender.sortable("cancel");
          }
      });
    }

    $('.sortable').sortable({
        connectWith: '.sortable',
        placeholder: 'widget_placeholder',
        revert: true,
        start: function(event, ui) {
            $('.widget_placeholder').append(ui.item.html());
            // $('.widget_placeholder').append(ui.item.context.outerHTML);
        },
        beforeStop: function(event, ui) {
          move(event, ui);
        },
        // stop: function(event, ui) {},
        // change: function(event, ui) {},
    }).disableSelection();
});
