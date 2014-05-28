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
                    $('#formfield-form-show_time').show();
                } else {
                    $('#formfield-form-show_time').hide();
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
        this.videogallery();
        this.cycle2();
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
    videogallery: function() {
        $('.portal-padrao-videogallery-portlet').each(function(){
            var $portlet = $(this);
            $('.portlet-videogallery-player', $portlet).each(function() {
                var $container = $(this);
                var $player = $('iframe', $container);
                var width = parseInt($container.width()) - (parseInt($container.css('padding-left')) * 2);
                var height = parseInt(width * 10 / 16);
                $player.width(width);
                $player.height(height);
            });
        });
    },
    cycle2: function() {
        if (!root.cycle2_loaded) {
            root.cycle2_loaded = true;

            var obj = this;
            $('.cycle-slideshow').on('cycle-next cycle-prev', function (e, opts) {
                var $galeria = $(this).parent().parent();
                var $slideshows = $('.cycle-slideshow', $galeria);
                $slideshows.not(this).cycle('goto', opts.currSlide);
                obj.layoutAdjustment($galeria, opts.currSlide);
            });

            // Aplicando o mesmo controle de navegacao para os thumbs e galerias
            $('.cycle-carrossel .thumb-itens').click(function (e){
                e.preventDefault();
                var $thumbs = $(this).parent().parent();
                var $galeria = $thumbs.parent().parent();
                var $slideshows = $('.cycle-slideshow', $galeria);
                var index = $thumbs.data('cycle.API').getSlideIndex(this);
                $slideshows.cycle('goto', index);
                obj.layoutAdjustment($galeria, index);
            });

            $('.cycle-pager .thumb-itens').click(function (e){
                e.preventDefault();
                var $thumbs = $(this).parent().parent();
                var $galeria = $thumbs.parent().parent();
                var $slideshows = $('.cycle-slideshow', $galeria);
                var index = parseInt($(this).data('slide-index'));
                $slideshows.cycle('goto', index);
                obj.layoutAdjustment($galeria, index);
            });

            // Adicionando navegação por teclado
            $(document.documentElement).keyup(function (event) {
                if (event.keyCode == 37) {
                    $('.cycle-prev').trigger('click');
                } else if (event.keyCode == 39) {
                    $('.cycle-next').trigger('click');
                }
            });

            $('.cycle-slideshow').each(function(){
                var $galeria = $(this).parent().parent();
                obj.layoutAdjustment($galeria, 0);
            });
        }
    },
    layoutAdjustment: function($galeria, index){
        var aElem = $(".cycle-player .cycle-slide", $galeria),
        elem,
        novaaltura,
        alturaimagem,
        larguracarosel;

        // Pula primeiro elemento
        index = index + 1;
        elem = aElem[index],
        novaaltura = $(elem).height();
        alturaimagem = $('.cycle-sentinel img', $galeria).height();
        larguracarosel = ($('.carousel', $galeria).width() -
                          (36 * 2));

        $('.cycle-sentinel', $galeria).height(novaaltura);
        $('.cycle-hover', $galeria).height(alturaimagem);
        $('.cycle-carrossel', $galeria).width(larguracarosel);
    },
};

