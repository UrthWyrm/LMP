const http = require('http');
const { exec } = require('child_process');
const fs = require('fs');

//create a server object:
http.createServer(function (req, res) {

  //if the request url is: localhost:5000
  if(req.url === "/"){
    fs.readFile("dashboard.html", function(err, data){
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      res.end();
    });
  //if the request url is: localhost:5000/run
  }else if(req.url === "/run"){


    exec('./ /home/techm/Documents/labelImg-master/run.sh', (error, stdout, stderr) => {
     if (error) {
       console.error(`exec error: ${error}`);
       res.write('Command has failed'); //write a response to the client
       res.end(); //end the response
       return;
     }
     console.log(`stdout: ${stdout}`);
     console.log(`stderr: ${stderr}`);

     res.write('Command has been run'); //write a response to the client
     res.end(); //end the response
    });
  }

}).listen(5000); //the server object listens on port 5000