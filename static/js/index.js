$(document).ready(function(){


    $("button").click(function(){
    
    var CLIENT_ID = "b01b5772ca9645c49cb374febc690a0b";
    var REDIRECT_URI = "http://localhost:5000/LikeMyPics/dashboard.html";
    
    var url = "https://api.instagram.com/oauth/authorize/?client_id="+ CLIENT_ID + "&redirect_uri="+REDIRECT_URI+"&response_type=code&scope=basic+likes+comments+follower_list+public_content";
    
    window.location = url;
    
    });  
    
    });
    