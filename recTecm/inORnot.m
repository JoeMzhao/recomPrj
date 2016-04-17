function a = inORnot(timestamp)
    
    global poolSize

thre = 1 - poolSize/timestamp;
buff = rand(1);

if buff < thre
    a = 1;
else
    a = 0;
end


