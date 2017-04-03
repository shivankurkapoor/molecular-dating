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

function upload(form) {
    alert("Inside upload")
    if (form.id == 'ss_single_form') {
        if (!isAnyError()) {
            var formtype = 'single';
            var datatype = 'ss';
            var align = form.elements['align'].value;
            var hxb2 = form.elements['hxb2'].value;
            var fastafile = form.elements['fastafile'].files[0];
            var formdata = new FormData();
            formdata.append('formtype', formtype);
            formdata.append('datatype', datatype);
            formdata.append('align', align);
            formdata.append('hxb2', hxb2);
            formdata.append('fastafile', fastafile);

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