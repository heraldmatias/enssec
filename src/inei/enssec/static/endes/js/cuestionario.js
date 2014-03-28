/**
 * Created with PyCharm.
 * User: holivares
 * Date: 25/03/14
 * Time: 05:52 PM
 * To change this template use File | Settings | File Templates.
 */

    var blank = new RegExp('\\s{2}', 'g'),
        letter = new RegExp('^[A-Za-zñÑá-úÁ-Ú ]+$'),
        rletter = new RegExp('[^A-Za-zñÑá-úÁ-Ú ]','g'),
        number = new RegExp('[0-9][0-9]$'),
        rnumber = new RegExp('[^0-9]','g');

    $(document).on('ready', function(e){
        $("#id_consulado_list").chosen({
            no_results_text: "No se encontro el proyecto!",
            allow_single_deselect: true
        }).change(function(e){
            $('#id_fecha_day').focus();
        });
        $("#id_pais_list").chosen({
            no_results_text: "No se encontro el proyecto!",
            allow_single_deselect: true
        }).change(function(e){
            $('#id_ciudadResidencia').focus();
        });
        $('#id_ficha').focus();
        nextControlEnter();
    });

    $('select').on('change', function(e){
        var valor = $(this).val();
        if(valor !== '' ){
            $('#l'+this.id).removeClass('alert-error');
        }else{
            $('#l'+this.id).addClass('alert-error');
        }
    });

    $("#id_pais_list").on('change', function(){
        var value = $(this).val();
        value = value.split('-');
        $('#id_continente').val(value[2]);
    });

    $('#id_nu_respuesta1_5').on('change', function(){
        var txtOtro = $('#id_no_respuesta1_6');
        var checked = $(this).is(':checked');
           if(checked){
               txtOtro.prop('readonly', false);
           }else{
               txtOtro.val('');
               txtOtro.prop('readonly', true);
           }
    });

    $('input[name="nu_respuesta1_6"]').on('keypress', function(e){
        if(e.which === 13){
            var txtOtro = $('#id_no_respuesta1_6');
            if($(this).val()==='1'){
                txtOtro.prop('readonly', false);
                txtOtro.focus();
            }else{
                txtOtro.val('');
                txtOtro.prop('readonly', true);
                $('#id_nu_respuesta2').focus();
            }
        }
    });

    $('input[name="nu_respuesta6"]').on('keypress', function(e){
        if(e.which === 13){
            var txtOtro = $('#id_no_respuesta6');
            $('#lid_nu_respuesta6').removeClass('alert-error');
            if($(this).val()==='6'){
                txtOtro.prop('readonly', false);
                txtOtro.focus();
            }else{
                txtOtro.val('');
                txtOtro.prop('readonly', true);
                $('#id_encuestado').focus();
            }
        }
    });

    $('input[name="tomo"]').on('change', function(e){
        $('#lid_tomo').removeClass('alert-error');
    });

    $('input[name="ficha"]').on('change', function(e){
        $('#lid_ficha').removeClass('alert-error');
    });

    $('input[name="nu_respuesta2"]').on('change', function(e){
        $('#lid_nu_respuesta2').removeClass('alert-error');
    });

    $('input[name="nu_respuesta3"]').on('change', function(e){
        $('#lid_nu_respuesta3').removeClass('alert-error');
    });

    $('input[name="nu_respuesta4"]').on('change', function(e){
        $('#lid_nu_respuesta4').removeClass('alert-error');
    });

    $('input[name="nu_respuesta5"]').on('change', function(e){
        $('#lid_nu_respuesta5').removeClass('alert-error');
    });

    $('.texto').on('input blur', function(e){
        var valor = $(this).val().toUpperCase();
        if(valor !== '' ){
            if(!blank.test(valor) && letter.test(valor)){
                $(this).val(valor);
                $('#l'+this.id).removeClass('alert-error');
                $(this).tooltip('hide');
            }else{
                valor = $.trim(valor.replace(blank, ' ').replace(rletter, ''));
                $(this).val(valor);
            }
        }else{
            $('#l'+this.id).addClass('alert-error');
        }
    });

    $('.numero').on('input blur', function(e){
        var valor = $(this).val();
        if(valor !== '' ){
            if(!blank.test(valor) && number.test(valor)){
                $(this).val(valor);
                $('#l'+this.id).removeClass('alert-error');
                $(this).tooltip('hide');
            }else{
                valor = $.trim(valor.replace(blank, '').replace(rnumber, ''));
                $(this).val(valor);
            }
        }else{
            $('#l'+this.id).addClass('alert-error');
        }
    });

    function buscar_cuestionario(){
        var data = $('#id_form').serialize();
        var options = {
            type: 'POST',
            url: '/enssec/cuestionario/ajax/',
            dataType: 'json',
            async: true,
            data: data,
            beforeSend: function() {
            }
        };
        var posting = $.ajax(options);
        posting.done(function(data, textStatus, jqXHR) {
            if(data['success']){
                 location.href = '/enssec/cuestionario/'+ data['data'] +'/';
            }else{
                alert(data['data']);
                location.href = '/enssec/cuestionario/';
            }
        })
        .fail(function(data, textStatus, jqXHR) {
            alert('Ha ocurrido un error inesperado'+textStatus);
        });
    }

    function save_cuestionario(){
        var data = $('#id_form').serialize();
        var options = {
            type: 'POST',
            url: location.href,
            dataType: 'json',
            async: true,
            data: data,
            beforeSend: function() {

            }
        };
        var posting = $.ajax(options);

        posting.done(function(data, textStatus, jqXHR) {
            if(data['success']){
                location.href = '/enssec/cuestionario/';
            }else{
                //activate_tooltips();
                $('.alert-error').removeClass('alert-error');
                var msg='Corrija los errores marcados en rojo porfavor!';
                if(data['data']==='duplicado'){
                    alert('Ya existe la ficha y tomo digitado en el consulado');
                    $('#lid_ficha').addClass('alert-error');
                    $('#lid_tomo').addClass('alert-error');
                }else{
                $.each(data['data'],function(k,v){
                    if($.inArray(k, ['nu_respuesta1_1','nu_respuesta1_2','nu_respuesta1_3','nu_respuesta1_4','nu_respuesta1_5','nu_respuesta1_6']) !== -1){
                        $('#id_'+k).parent().addClass('alert-error');
                    }else if (k === 'no_respuesta1_6'){
                        $('#id_nu_respuesta1').addClass('alert-error');
                    }else if (k === 'no_respuesta6'){
                        $('#id_nu_respuesta6').addClass('alert-error');
                    }else if (k === '__all__'){
                        alert(v[0]);
                        $('#lid_tomo').addClass('alert-error');
                        $('#lid_ficha').addClass('alert-error');
                    }else if (k === 'dni'){
                        if(v[0].indexOf('existe') !== -1)
                            alert(v[0]);
                        $('#lid_'+k).addClass('alert-error');
                    }else{
                        $('#lid_'+k).addClass('alert-error');
                    }
                });
                alert(msg);
                }
            }
        })
        .fail(function(data, textStatus, jqXHR) {
            alert('Ha ocurrido un error inesperado'+textStatus);
        });
    }

    $('.bit').on('keypress', function(e){
        if($.inArray($(this).val(), ['0', '1']) === -1){
            $(this).parent().addClass('alert-error');
        }else{
            $(this).parent().removeClass('alert-error');
        }
    });

    function nextControlEnter(){
        //$('#id_consulado_list_chosen').addClass('chosen-disabled');
        var textoSiguiente = Array();
        textoSiguiente['id_ficha'] = [1, '#id_fecha_day', true];
        textoSiguiente['id_fecha_day'] = [1, '#id_fecha_month', true];
        textoSiguiente['id_fecha_month'] = [1, '#id_fecha_year', true];
        textoSiguiente['id_fecha_year'] = [2, '#id_pais_list', true];
        textoSiguiente['id_ciudadResidencia'] = [1, '#id_edad', true];
        textoSiguiente['id_edad'] = [1, '#id_sexo', true];
        textoSiguiente['id_sexo'] = [1, '#id_nu_respuesta1_1', true];
        textoSiguiente['id_nu_respuesta1_1'] = [1, '#id_nu_respuesta1_2', true];
        textoSiguiente['id_nu_respuesta1_2'] = [1, '#id_nu_respuesta1_3', true];
        textoSiguiente['id_nu_respuesta1_3'] = [1, '#id_nu_respuesta1_4', true];
        textoSiguiente['id_nu_respuesta1_4'] = [1, '#id_nu_respuesta1_5', true];
        textoSiguiente['id_nu_respuesta1_5'] = [1, '#id_nu_respuesta1_6', true];
//        textoSiguiente['id_nu_respuesta1_6'] = [1, '#id_no_respuesta1_6', true];
        textoSiguiente['id_no_respuesta1_6'] = [1, '#id_nu_respuesta2', true];
        textoSiguiente['id_nu_respuesta2'] = [1, '#id_nu_respuesta3', false];
        textoSiguiente['id_nu_respuesta3'] = [1, '#id_nu_respuesta4', true];
        textoSiguiente['id_nu_respuesta4'] = [1, '#id_nu_respuesta5', true];
        textoSiguiente['id_nu_respuesta5'] = [1, '#id_nu_respuesta6', true];
//        textoSiguiente['id_nu_respuesta6'] = [1, '#id_no_respuesta6', true];
        textoSiguiente['id_no_respuesta6'] = [1, '#id_encuestado', true];
        textoSiguiente['id_encuestado'] = [1, '#id_dni', true];
        textoSiguiente['id_dni'] = [1, '#id_observacion', true];
        textoSiguiente['id_observacion'] = [1, '#id_dni', true];
        textoSiguiente['id_observacion'] = [1, '#grabar', true];
        var cajas = $('input[type="text"], select, textarea');
        var campoSiguiente = null;

        $.each(cajas, function(i, c){
            if(textoSiguiente[c.id] !== undefined){
            $(c).on('keypress', function(e){
                if(e.which === 13){
                    var iScroll = jQuery(window).scrollTop();
                    campoSiguiente = $(textoSiguiente[c.id][1]);
                    if(textoSiguiente[c.id][0]===2){
                        campoSiguiente.trigger('chosen:activate');
                    }else{
                        campoSiguiente.focus();
                    }
                    if(textoSiguiente[c.id][2]===true){
                        iScroll = iScroll + 40;
                        jQuery('html, body').animate({  scrollTop: iScroll }, 200);
                    }
                }
            });
            }
        });
    }
