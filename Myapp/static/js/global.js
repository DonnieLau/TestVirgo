function display_menu() {
    var menu = document.getElementById("navbar");
    var btnself = document.getElementById("menu_btn");
    if (btnself.innerText == '<') {
        menu.style.display = 'none';
        btnself.style.left = '0px';
        btnself.innerText = '>';
    } else {
        menu.style.display = 'block';
        btnself.style.left = '188px';
        btnself.innerText = '<';
    }
}

function show_upload() {
    document.getElementById("upload_file").style.display = 'block';
}