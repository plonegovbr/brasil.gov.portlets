var root = typeof exports !== "undefined" && exports !== null ? exports : this;

$(function() {
    portlets.init();
});

var portlets = {
    init: function() {
        this.collection()
    },
    collection: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Coleção') > 0) {
            var update_image = function() {
                if ($('#form\\.show_image').is(':checked')) {
                    $('#formfield-form-image_size').show();
                } else {
                    $('#formfield-form-image_size').hide();
                }
            };
            var update_footer = function() {
                if ($('#form\\.show_footer').is(':checked')) {
                    $('#formfield-form-footer').show();
                    $('#formfield-form-footer_url').show();
                } else {
                    $('#formfield-form-footer').hide();
                    $('#formfield-form-footer_url').hide();
                }
            };
            var update_date = function() {
                if ($('#form\\.show_date').is(':checked')) {
                    $('#formfield-form-date_format').show();
                } else {
                    $('#formfield-form-date_format').hide();
                }
            }
            var insert_collection_warning = function() {
                var html = '<div>' +
                           '    <span class="warning">' +
                           '        ATENÇÃO: Para coleções de Evento ou Compromisso (Agenda), será utilizada a data do Evento/Compromisso para ordenação e exibição, e não a data informada na coleção.' +
                           '     </span>' +
                           '</div>';
                $('#formfield-form-collection fieldset').append(html);
            }
            $('#form\\.show_image').on('click', update_image);
            $('#form\\.show_footer').on('click', update_footer);
            $('#form\\.show_date').on('click', update_date);
            update_image();
            update_footer();
            update_date();
            insert_collection_warning();
        }
    }
};

