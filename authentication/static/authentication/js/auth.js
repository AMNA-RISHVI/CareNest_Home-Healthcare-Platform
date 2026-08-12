console.log("CareNest Authentication Loaded");

const step1Fields = [
    document.getElementById("id_full_name"),
    document.getElementById("id_username"),
    document.getElementById("id_email"),
    document.getElementById("id_phone")
];


nextBtn.addEventListener("click", function () {
    let valid = true;
    step1Fields.forEach(function (field) {
        if (field.value.trim() === "") {
            valid = false;
            field.classList.add("is-invalid");
        } else {
            field.classList.remove("is-invalid");
        }
    });


    /* --------------------------------
       Do not move to Step 2
       if Step 1 is invalid
    -------------------------------- */
    if (!valid) {
        return;
    }

    /* --------------------------------
       Move to Step 2
    -------------------------------- */
    step1.classList.remove("active");
    step2.classList.add("active");

    /* --------------------------------
       Update indicators
    -------------------------------- */
    indicator1.classList.add("active");
    indicator1.classList.add("completed");
    indicator2.classList.add("active");

    /* --------------------------------
       Step 2 = 50%
    -------------------------------- */
    progressFill.style.width = "50%";
});


/* ==========================================
   BACK BUTTON
========================================== */
if (backBtn) {
    backBtn.addEventListener("click", function () {
        step2.classList.remove("active");
        step1.classList.add("active");
        indicator2.classList.remove("active");

        /* Back to Step 1 = 0% */
        progressFill.style.width = "0%";
    });
}


const password=document.getElementById("id_password1");
const fill=document.getElementById("strengthFill");
const text=document.getElementById("strengthText");

password.addEventListener("keyup",function(){
    const value=password.value;
    let score=0;
    if(value.length>=8) score++;
    if(/[A-Z]/.test(value)) score++;
    if(/[0-9]/.test(value)) score++;
    if(/[^A-Za-z0-9]/.test(value)) score++;

    if(score==1){
        fill.style.width="25%";
        fill.style.background="red";
        text.innerHTML="Weak";
    }

    else if(score==2){
        fill.style.width="50%";
        fill.style.background="orange";
        text.innerHTML="Fair";
    }

    else if(score==3){
        fill.style.width="75%";
        fill.style.background="#18B394";
        text.innerHTML="Good";
    }

    else if(score==4){
        fill.style.width="100%";
        fill.style.background="#0B8F88";
        text.innerHTML="Strong";
    }

});

const imageInput = document.getElementById("id_profile_picture");
const preview = document.getElementById("profilePreview");

if(imageInput){
    imageInput.addEventListener("change",function(){
        const file=this.files[0];
        if(file){
            preview.src=URL.createObjectURL(file);
        }
    });
}

document.querySelectorAll(".toggle-password").forEach(icon=>{
    icon.addEventListener("click",function(){
        const input=document.getElementById(this.dataset.target);

        if(input.type==="password"){
            input.type="text";
            this.classList.replace("fa-eye","fa-eye-slash");
        }
        else{
            input.type="password";
            this.classList.replace("fa-eye-slash","fa-eye");
        }

    });
});


function updateRule(id, passed){
    const rule=document.getElementById(id);
    if(!rule) return;
    if(passed){
        rule.classList.add("valid");
        rule.innerHTML="✔ "+rule.innerHTML.substring(2);
    }else{
        rule.classList.remove("valid");
        rule.innerHTML="✖ "+rule.innerHTML.substring(2);
    }
}


password.addEventListener("keyup",function(){
    const value=password.value;

    updateRule("lengthRule",value.length>=8);
    updateRule("upperRule",/[A-Z]/.test(value));
    updateRule("lowerRule",/[a-z]/.test(value));
    updateRule("numberRule",/[0-9]/.test(value));
    updateRule("specialRule",/[^A-Za-z0-9]/.test(value));
});


const firstError=document.querySelector(".field-error");

if(firstError){
    const input=firstError.previousElementSibling;
    if(input){
        input.focus();
        input.scrollIntoView({
            behavior:"smooth",
            block:"center"
        });
    }
}