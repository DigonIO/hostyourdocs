////////////////////////////////////////////////////////////////////////////////////////////////////
//// Template Variables
////////////////////////////////////////////////////////////////////////////////////////////////////

const root_path = "{{ root_path }}"
const footer_content_path = "{{ footer_content_path }}"

////////////////////////////////////////////////////////////////////////////////////////////////////
//// Loader Script
////////////////////////////////////////////////////////////////////////////////////////////////////

let folder_offset = root_path.split("/").length

const path_elements = window.location.pathname.split("/")

const project = path_elements[1 + folder_offset]
const is_tag = path_elements[2 + folder_offset] === "t"
const tag_ver = path_elements[3 + folder_offset]

var request = root_path + footer_content_path
request += `?project_name=${project}&is_tag=${is_tag}&tag_ver=${tag_ver}`

function inject_footer(html_code) {
    var footer = document.createElement("div")
    footer.innerHTML = html_code
    document.body.appendChild(footer)
}

fetch(request)
    .then(function (response) {
        response.text()
            .then(inject_footer)
    })


////////////////////////////////////////////////////////////////////////////////////////////////////
//// Menu Script
////////////////////////////////////////////////////////////////////////////////////////////////////

var hyd_menu_open = false

function hyd_toggle_menu() {
    const hyd_button = document.getElementById('hyd-button');
    const hyd_menu = document.getElementById('hyd-menu');

    if (hyd_menu_open === true) {
        hyd_menu.classList.add("hyd-hidden");
        hyd_button.classList.remove("hyd-hidden");
        hyd_menu_open = false
    } else {
        hyd_menu.classList.remove("hyd-hidden");
        hyd_button.classList.add("hyd-hidden");
        hyd_menu_open = true
    }
}

function hyd_close_menu(event) {
    const hyd_footer = document.getElementById('hyd-footer');
    if (!hyd_footer.contains(event.target) && hyd_menu_open) {
        hyd_toggle_menu()
    }
}

document.addEventListener("click", hyd_close_menu);