var malicious_list = new Array();
var normal_list = new Array();



document.addEventListener("DOMContentLoaded", function(){


    chrome.tabs.executeScript({
        code:'document.getElementById("readFrame").innerHTML'
    }, function(result){
       //let data = result[0];
       const request = new XMLHttpRequest();
       request.open('POST', 'http://127.0.0.1:5000/data', true);
       //request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded;charset=UTF-8'); 
       request.setRequestHeader('Content-type', 'text/plain;charset=UTF-8'); 
       request.send("data=" + result[0]);  
       request.onreadystatechange = function(event){ 
        if(request.readyState == 4 && request.status == 200){
         
            //document.getElementById("results").innerHTML = request.responseText;
            
            const responseData = request.responseText
            const responseJson = JSON.parse(responseData);
            var urls = new Array(); // url 배열
            // var malicious_list = new Array();
            // var normal_list = new Array();
            for (json in responseJson){
                urls.push(json)
            }
            // document.getElementById("results").innerHTML = 
            // urls[0] + ":" + responseJson[urls[0]] + " & " + urls[1] + ":" + responseJson[urls[1]];

            for (var i in urls){
               
                if(responseJson[urls[i]] == "malicious"){
                    malicious_list.push(urls[i])
                }else{
                    normal_list.push(urls[i])
                }
            }



            var mal_string = ""
            var normal_string = ""
            for (var m in malicious_list){
                if (  malicious_list[m] !== undefined)
                    {
                        mal_string  += malicious_list[m] + "<br>";
                    }
           
                //document.getElementById("malicious_results").innerHTML += malicious_list[m] + "<br>";
            }

            for ( var m in normal_list){
                 if ( normal_list[m] !== undefined){
                 normal_string  += normal_list[m] + "<br>";
                   }
                //document.getElementById("normal_results").innerHTML += normal_list[m] + "<br>";
            }
            
            //document.getElementById("malicious_results").innerHTML = malicious_list;
            //document.getElementById("normal_results").innerHTML = normal_list;
        
                document.getElementById("malicious_results").innerHTML = mal_string;
                document.getElementById("normal_results").innerHTML = normal_string;
        }
    }
 

    });
 
});
