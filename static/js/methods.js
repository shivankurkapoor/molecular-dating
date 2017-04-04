function openForm(evt, sequenceDataType) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(sequenceDataType).style.display = "block";
    evt.currentTarget.className += " active";
}

function showDefault() {
    //Setting Sanger Sequencing tab content on display by default
    button = document.getElementById("ssbutton");
    tabcontent = document.getElementById("ss");
    tabcontent.style.display = "block";
    button.className += " active";
}

function isAnyError(form) {
    return false;
}

function upload(form) {
    var requests = [];
    if (form.id == 'ss_single_form') {
        if (!isAnyError(form)) {
            var formtype = 'single';
            var datatype = 'ss';
            var request = Object();
            request.file = 'fastafile_1';
            request.align = form.elements['align'].checked;
            request.hxb2 = form.elements['hxb2'].checked;
            var fastafile = form.elements['fastafile'].files[0];
            var numreq = 1;
            requests.push(request);
            var formdata = new FormData();
            formdata.append('formtype', formtype);
            formdata.append('datatype', datatype);
            formdata.append('formdata', JSON.stringify({'requests':requests}));
            formdata.append('numreq', numreq);
            formdata.append('fastafile_1', fastafile);

            $.ajax({
                url: '/upload',
                data: formdata,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function (data) {
                    alert(data);
                    window.location.href = "/showform";
                }
            });


        }
    }
    else if (form.id == '') {

    }
    else if (form.id == '') {

    }
    else if (form.id == '') {

    }
    return false
}