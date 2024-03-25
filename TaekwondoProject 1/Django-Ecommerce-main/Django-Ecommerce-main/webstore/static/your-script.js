const fullName = document.getElementById('Name');
const email = document.getElementById('Email');
const contact = document.getElementById('Contact');
const problem = document.getElementById('problem');

function sendEmail() {

    const bodyMessage = `Full Name: ${fullName.value}<br>
                         Email: ${email.value}<br>
                         Contact: ${contact.value}<br>
                         Message: ${problem.value}`;
    

    Email.send({
        Host: "smtp.elasticemail.com",
        Username: "sahilavinashjadhav2003@gmail.com",
        Password: "F85BE669DA2D2BA2B2F76557E1252EF5B577",
        To: 'sahilavinashjadhav2003@gmail.com',
        From: "sahilavinashjadhav2003@gmail.com",
        Subject: "New enquire mail",
        Body: bodyMessage
    }).then(
        message =>{
            if(message == "OK"){
                Swal.fire({
                    title: "Success",
                    text: "Message sent successfully!",
                    icon: "success"
                  });
            }
        }
    )
}

function checkInputs(){
    const items = document.querySelectorAll(".item");

    for(const item of items){
        if (item.value == ""){
            item.classList.add("error");
            item.parentElement.classList.add("error");
        }
    }
}

function checkInputValue(input) {
    var label = input.nextElementSibling;
    if (input.value !== "") {
        label.classList.add('active');
    } else {
        label.classList.remove('active');
    }
}


document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");
});

document.addEventListener('DOMContentLoaded', function () {

    console.log("THIS DOM CONTENT IS GETTING EXCUTED")

    // Your code Snippet #1

    const barsIcon = document.querySelector('.checkbtn');
    const navList = document.getElementById('navList');

    barsIcon.addEventListener('click', function () {
        console.log("clicked on barIcon");
        navList.classList.toggle('show');
    });




    // Your code Snippet #2

    // const menuIcon = document.getElementById('menuIcon');
    // const navList2 = document.querySelector('.navdiv ul');

    // menuIcon.addEventListener('click', () => {
    //     console.log("clicked on menuIcon");
    //     navList2.classList.toggle('show');
    // });

    // Your code Snippet #3

    const minorButton = document.getElementById('minorButton');
    const divsToToggle = document.querySelectorAll('#minorButton ~ div');

    minorButton.addEventListener('click', function() {
        divsToToggle.forEach(div => {
            console.log("clicked on minorButton");
            div.style.display = div.style.display === 'none' ? 'block' : 'none';
        });
    });

    // Your code Snippet #4

    const form = document.querySelector('form');

    form.addEventListener("submit",(e) => {
        checkInputs();
    })
});

// let contacts = document.getElementById("contact");
// console.log(contacts.innerHTML);
// if(contacts.length < 10)
// {
//     alert("Do not enter additional numbers");
//     contacts.setAttribute = ("disabled");
// }
document.body.style.backgroundColor = "red";

