;include 'emu8086.inc'             
;.model small
;.stack 100h
;.data
;                        
;.code            
;
;main proc
;    
;   print 'Enter character : '
;   
;   mov ah, 01h    ;input
;   int 21h
;   
;   mov bl, al  
;   
;   
;   mov dl, 10    ;new line
;   mov ah, 02h    ;output
;   int 21h      
;   
;   mov dl, 13    ;carriage return
;   mov ah, 02h    ;output
;   int 21h  
;   
;   
;   print 'Your character : '   
;   
;   mov dl, bl
;   
;   mov ah, 02h    ;output
;   int 21h
;   
;    
;   mov ah, 04ch
;   int 21h
;    
;   main endp
;   
;end main
;
;    


include 'emu8086.inc'             
.model small
.stack 100h
.data 

msg db ?
                        
.code            

main proc   
    
   mov ax, @data
   mov ds, ax 
   
    
   print 'Enter character : '
   
   mov ah, 01h    ;input
   int 21h
   
   mov msg, al  
   
   
   mov dl, 10    ;new line
   mov ah, 02h    ;output
   int 21h      
   
   mov dl, 13    ;carriage return
   mov ah, 02h    ;output
   int 21h  
   
   
   print 'Your character : '   
   
   mov dl, msg
   
   mov ah, 02h    ;output
   int 21h
   
    
   mov ah, 04ch
   int 21h
    
   main endp
   
end main

