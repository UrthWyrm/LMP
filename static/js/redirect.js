$(document).ready(function(){


    var code = getCode("code");
    var result;
    
    
    var CLIENT_ID = "2106fa27fc544f96aa5e3e3b23f3d273";
    var REDIRECT_URI = "http://localhost:8080/SocialAuth/redirect.html";
    var CLIENT_SECRET = "a1a4da95b5d143c8ba5de8c5c8b5afb3";
    
    var url = "https://api.instagram.com/oauth/access_token";
    
    $.ajax({
        url:  url,
        type: "POST",
        data: 
        {
         client_id:CLIENT_ID,
         client_secret:CLIENT_SECRET,
         redirect_uri:REDIRECT_URI,
         grant_type:"authorization_code",
         code:code
        },
        async:false,
        success: function(data){
           console.log(data);
           result = 
           `
                <img src="${data.user.profile_picture}" class="img-rounded">
                <p>UserName: ${data.user.username}</p>
                Bio:<p>Bio: ${data.user.bio}</p>
                Website:<p>Website: ${data.user.website}</p>
               `;
           $("#result").append(result);
        }
     }
    );
    
    
    
    
    
    
    
    function getCode(c){
            var fullUrl = window.location.search.substring(1);
            var parametersArray = fullUrl.split("&");
            for(var i = 0; i<parametersArray.length;i++)
            {
                var currentParameter = parametersArray[i].split("=");
                if(currentParameter[0] == c){
                    return currentParameter[1];
                }
            }
        }
    
    
    });