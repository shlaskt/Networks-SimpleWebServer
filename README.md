# Networks_ex3
Web server . 
In that task we implemented a TCP server that functions as follows:  
The client sends a file name to the server that he wants to download (aka, the server sends it back).  
If the file name also contains a folder path, the server looks for the file according to the path within the files folder.  

The **format** the client sends to the server is the following format:
The first line says: *GET [Message] HTTP / 1.1*
When instead of "Message" the file name will be written.  
If file name is "/" (slash), then the file is named index.html.  
The client sends more lines in the message so the customer has finished sending the message when it sends a new line times, i.e. r \ n \ r \ n \.  

**Output:**  
1. If the file exists, the server will return:  
  *HTTP / 1.1 200 OK  
  Connection: [conn]   
  Content-Length: [length]
  Then a blank line, then the file's.*  
  Instead of [conn], the value of the *connection* field that was requested by the client will be listed, and instead of        [length], the size of the sent file will appear.

2. If the file does not exist, the server returns:  
  *HTTP/1.1 404 Not Found.  
  Connection: close*

3. If the client requested a file named *GET /redirect HTTP/1.1*, The server returns:    
  *HTTP/1.1 301 Moved Permanently.  
  Connection: close .   
  Location: /result.html*  
  
# How to run
* **Client**      
The client is the chrome browser, so just type in the browser's address bar the following:   
*[Server IP]:* *[Server port]* *[Path]*   
(the server's IP address, periodic, the port the server listens to, the path of the file)     
For example: *1.2.3.4:80/*   
This line addresses the server located at 1.2.3.4 and listens to Port 80 and requests the path "/"
(As defined above)  
*Notice - If you are running the server on your computer, you can instead the local IP address (127.0.0.1) to write localhost.*  
* **Server**      
The server receives one argument only - the port to which it listens.
