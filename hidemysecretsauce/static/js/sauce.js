function remove_sauce(sauce, sauce_button) {
    console.log(sauce_button);
    let sauce_id = sauce_button.getAttribute("sauce_id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/delete_sauce', true);

    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.addEventListener('load', function(event) {
        sauce.remove();
    } );
    let data = {"_id": sauce_id};
    xhr.send(JSON.stringify(data));

}

let sauces = document.getElementsByClassName("sauce");
for (let sauce of sauces) {
    let sauce_button = sauce.getElementsByClassName("remove-sauce")[0];
    sauce_button.addEventListener("click", () => remove_sauce(sauce, sauce_button));
}
