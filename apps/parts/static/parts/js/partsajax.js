// @ts-check

function refreshTree(){
    console.log('called refresh')
    $.ajax({
        url: $('#search_form').attr('action'), /* Where should this go? */
        method: 'post', /* Which HTTP verb? */
        data: $('#search_form').serialize(), /* Any data to send along? */
        success: function(serverResponse){
          console.log(serverResponse);
          $('#js_tree_box').jstree(true).settings.core.data = serverResponse;
          $('#js_tree_box').jstree(true).refresh();
          console.log('refresh success');
        }
    });
};

function refreshList(){
    var searchStr = $('#list_search_box').val();
    var data = {'search_text': searchStr}
    $.ajax({
        url: '/parts/getpartlist',
        method: 'get',
        data: data,
        success: function(resp){
            var selectOptions = ''
            for (var i = 0; i < resp.length; i++){
                selectOptions += `<option value="${resp[i].id}">Name: ${resp[i].name}</option>`;
            }
            $('#subPartSelect').html(selectOptions);

        }
    });
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addchild(){
    var r = $('#js_tree_box').jstree(true).get_selected();
    if (r.length > 0){
        r = r[0];
        console.log(r);
        var idInd = r.indexOf('_');
        if (idInd > 0){
            var parent_id = r.slice(idInd + 1)
        }else{
            var parent_id = r
        }
        console.log(parent_id)
        var token = getCookie('csrftoken');
        var child_id = $('#subPartSelect').val()
        if (child_id > 0){

            var postData = {
                'parent_id' : parent_id,
                'child_id' : child_id,
                'quantity' : $('#childQuantity').val(),
                'csrfmiddlewaretoken' : token,
            }
            $.ajax({
                url: '/parts/addchild/',
                method: 'post',
                data: postData,
                success: function(resp){
                    if (resp.status){
                        console.log(resp)
                        refreshTree()
                        console.log(r);
                        $('#js_tree_box').jstree('open_node', r);
                        $('.errorlist').remove();
                    }else{
                        $('.errorlist').remove();
                        $('#subpartSelect').prepend(`<p class="errorlist">${resp.message}</p>`)
                    }
                }
                
            });
        }

    }

};

function resetForm($form) {
    $form.find('input:text, input:password, input:file, select, textarea').val('');
    $form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
}

function getNewForm(){
    $('#edit_user_form').attr('action', '/parts/create/');
    $('#edit_user_form').attr('id', 'create_user_form');
    resetForm($('#create_user_form'))
    $('#otherErrors').empty();
    $('.errorlist').remove();
    $('#formTitle').children().html('Create Part Form');
    console.log('Got New Form')

};
function readyEdit(){

    $('#edit_user_form').submit(function(e){
        e.preventDefault()
        console.log('Sending Ajax request to', $(this).attr('action'))
        console.log('Submitting the following data', $(this).serialize())
        $.ajax({
            url: $(this).attr('action'), /* Where should this go? */
            method: 'post', /* Which HTTP verb? */
            data: $(this).serialize(), /* Any data to send along? */
            success: function(serverResponse) { /* What code should we run when the server responds? */
                console.log(serverResponse)
                var respDict = serverResponse
                console.log(respDict)
                if (respDict.status){
                    $('#otherErrors').empty();
                    $('.errorlist').remove();
                    $('#otherErrors').append(`<p>${respDict.message}</p>`);
                    refreshTree();
                    refreshList();
                } else {
                    $('#otherErrors').append(`<p>${respDict.message}</p>`);
                }
            }
        })
    });
}

$(document).ready(function(){
    refreshList();
    $('#list_search_box').keyup(function(e){
        refreshList();
    });

    $('#delete_part').click(function(){
        var r = $('#js_tree_box').jstree(true).get_selected();
        if (r.length > 0){
            r = r[0];
            console.log(r);
            var idInd = r.indexOf('_');
            if (idInd > 0){
                var the_id = r.slice(idInd + 1)
            }else{
                the_id=r
            }
            var token = getCookie('csrftoken');
            var confirm = window.confirm(`Delete selected part?`)
            if (confirm) {

                $.ajax({
                    url: '/parts/deletepart/',
                    method: 'post',
                    data: {
                        'part_id':the_id,
                        'csrfmiddlewaretoken':token,
                    },
                    success:function(resp){
                        console.log(resp);
                        $('.errorlist').remove();
                        refreshTree();
                        refreshList();
                        getNewForm();
                    }
                })
            }
        }        
    });
    $('#remove_child').click(function(e){
        var r = $('#js_tree_box').jstree(true).get_selected();
        if (r.length > 0){
            r = r[0];
            console.log(r);
            var idInd = r.indexOf('_');
            if (idInd > 0){
                var child_id = r.slice(idInd + 1)
                var parent_id = r.slice(0, idInd)
            }
            console.log(parent_id)
            var token = getCookie('csrftoken');
            $.ajax({
                url: '/parts/removechild/',
                method: 'post',
                data: {
                    'parent_id':parent_id,
                    'child_id':child_id,
                    'csrfmiddlewaretoken':token,
                },
                success:function(resp){
                    if (resp.status){

                        console.log(resp);
                        $('.errorlist').remove();
                        refreshTree();
                    }else{
                        $('#search_form_area').prepend(`<p class="errorlist">${resp.message}</p>`)
                    }
                }
            })
        }
    });
    $('#js_tree_box')
    // listen for event
    .on('changed.jstree', function (e, data) {
        var r = $('#js_tree_box').jstree(true).get_selected();
        if (r.length > 0){
            r = r[0];
            console.log(r);
            var idInd = r.indexOf('_');
            if (idInd > 0){
                var parent_id = r.slice(idInd + 1)
            }else{
                var parent_id = r
            }
            console.log(parent_id)
            $.ajax({
                url: `/parts/${parent_id}/edit`,
                method: 'get',
                success: function(resp){
                    console.log('success', resp)
                    $('#formBody').html(resp);
                    $('#formTitle').children().html('Edit Part Form')
                    readyEdit();
                }
            });  
        }
    });
    $('#edit_user_form').on('submit', this, function(e){
        e.preventDefault()
        console.log('Sending Ajax request to', $(this).attr('action'))
        console.log('Submitting the following data', $(this).serialize())
        $.ajax({
          url: $(this).attr('action'), /* Where should this go? */
          method: 'post', /* Which HTTP verb? */
          data: $(this).serialize(), /* Any data to send along? */
          success: function(serverResponse) { /* What code should we run when the server responds? */
            console.log(serverResponse)
            var respDict = serverResponse
            console.log(respDict)
            if (respDict.status){
                $('#otherErrors').empty();
                $('.errorlist').remove();
                $('#otherErrors').append(`<p>${respDict.message}</p>`);
                refreshTree();
                refreshList();
            } else {
                $('#otherErrors').append(`<p>${respDict.message}</p>`);
            }
          }
        })
    });
    $('#create_user_form').on('submit', this, function(e){
        e.preventDefault()
        console.log('Sending Ajax request to', $(this).attr('action'))
        console.log('Submitting the following data', $(this).serialize())
        $.ajax({
          url: $(this).attr('action'), /* Where should this go? */
          method: 'post', /* Which HTTP verb? */
          data: $(this).serialize(), /* Any data to send along? */
          success: function(serverResponse) { /* What code should we run when the server responds? */
            console.log(serverResponse)
            var respDict = serverResponse
            console.log(respDict)
            if (respDict.status){
                $('#create_user_form').attr('action', respDict.action);
                $('#create_user_form').attr('id', 'edit_user_form');
                $('#otherErrors').empty();
                $('.errorlist').remove();
                $('#otherErrors').append('<p>Part saved</p>');
                refreshTree();
                refreshList();
                $('#formTitle').children().html('Edit Part Form')
            } else {
                if ('form' in respDict){
                    $('#form_contents').html(respDict.form);
                }else{
                    $('#otherErrors').empty();
                    for (var key in respDict){
                        if (key != 'status'){
                            $('#otherErrors').append(`<p>${respDict[key]}</p>`);
                        }
                    }
                }
            }
          }
        })
    });
    $.ajax({
        url: $('#search_form').attr('action'),
        method: 'post',
        data: $('#search_form').serialize(),
        success: function(serverResponse){
            // console.log(serverResponse)
            $('#js_tree_box').jstree({ 'core' : {
                'data' : serverResponse,
                'multiple' : false
            }});
        }
    });
    $('#search_form').submit(function(e){
        e.preventDefault()
        console.log('Sending Ajax request to', $(this).attr('action'))
        console.log('Submitting the following data', $(this).serialize())
        $.ajax({
          url: $(this).attr('action'), /* Where should this go? */
          method: 'post', /* Which HTTP verb? */
          data: $(this).serialize(), /* Any data to send along? */
          success: function(serverResponse){
            console.log(serverResponse);
            $('#js_tree_box').jstree(true).settings.core.data = serverResponse;
            $('#js_tree_box').jstree(true).refresh();
            
          }
        });
    });
});