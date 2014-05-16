var root = typeof exports !== "undefined" && exports !== null ? exports : this;

$(function() {
    portletsManager.init();
    portlets.init();
});

var portletsManager = {
    init: function() {
        this.collection();
        this.audiogallery();
        this.video();
        this.videogallery();
        this.mediacarousel();
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
    },
    audiogallery: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Galeria de Áudios') > 0) {
            var update_title = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                    $('#formfield-form-header_type').show();
                } else {
                    $('#formfield-form-header').hide();
                    $('#formfield-form-header_type').hide();
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
            $('#form\\.show_header').on('click', update_title);
            $('#form\\.show_footer').on('click', update_footer);
            update_title();
            update_footer();
        }
    },
    video: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Vídeo') > 0) {
            var update_title = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                } else {
                    $('#formfield-form-header').hide();
                }
            };
            $('#form\\.show_header').on('click', update_title);
            update_title();
        }
    },
    videogallery: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Galeria de Vídeos') > 0) {
            var update_header = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                    $('#formfield-form-header_type').show();
                } else {
                    $('#formfield-form-header').hide();
                    $('#formfield-form-header_type').hide();
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
            $('#form\\.show_header').on('click', update_header);
            $('#form\\.show_footer').on('click', update_footer);
            update_header();
            update_footer();
        }
    },
    mediacarousel: function() {
        if ($('h1.documentFirstHeading').text().indexOf('Portal Padrão Carrossel de Imagens') > 0) {
            var update_header = function() {
                if ($('#form\\.show_header').is(':checked')) {
                    $('#formfield-form-header').show();
                    $('#formfield-form-header_type').show();
                } else {
                    $('#formfield-form-header').hide();
                    $('#formfield-form-header_type').hide();
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
            $('#form\\.show_header').on('click', update_header);
            $('#form\\.show_footer').on('click', update_footer);
            update_header();
            update_footer();
        }
    },
};

var portlets = {
    init: function() {
        this.audiogallery();
        this.audio();
        this.mediacarousel();
    },
    audiogallery: function() {
        $('.portal-padrao-audiogallery-portlet').each(function(){
            $('#'+this.id).audiogallery();
        });
    },
    audio: function() {
        $('.portal-padrao-audio-portlet').each(function(){
            var playerid = $('#'+this.id+' .jp-jplayer')[0].id;
            var containerid = $('#'+this.id+' .jp-audio')[0].id;
            $('#'+playerid).audio_player({'cssSelectorAncestor':'#'+containerid});
        });
    },
    mediacarousel: function() {
        $('.portal-padrao-mediacarousel-portlet .portletItem>div:first').each(function(){
            $('#'+this.id).mediacarousel();
        });
    },
};

