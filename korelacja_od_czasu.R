


this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)


processLine = function(con) {
  
  line = readLines(con, n = 1)
  line.vec<-sub("\\[","(",line)
  line.vec<-sub("\\]",")",line.vec)
  line.vec<-paste0("c",line.vec)
  true.vec<- eval(parse(text = line.vec))
  
  return(true.vec)
}
processBigFile<-function(filepath){
  iteration.numbers<-c()
  distributions<-list()
  con = file(filepath, "r")
  i<-1
  while(TRUE)
  {
    iii = readLines(con, n = 1)
    if(length(iii)==0){break()}
    iteration.numbers<-c(iteration.numbers,iii)
    distro<-processLine(con = con)
    distributions[[i]]<-distro
    i<-i+1
  }
  close(con)
  return(list(iteration.numbers,distributions))
}



wykresy<-processBigFile("data_test_corr_max_zmniejsz/d_0.02_scale_38noise_change/d_0.02_corr_of_time.txt")
km<-c(10^1,10^1.2,10^1.4,10^1.6,10^1.8,10^2,10^2.2,10^2.4,10^2.6,10^2.8)
colors<-c("","red","blue","green","grey")
vvv<-plot(y = wykresy[[2]][[1]],x = km, main = "korelacja od odleglosci w czasie 10% populacji d= 0.02", log = "x",ylab = "korelacja")

for (i in 2:length(wykresy[[1]]))
{
  vvv<-vvv+lines(y = wykresy[[2]][[i]], x = km, col = colors[i])  
       
}

legend("bottomleft", legend=paste0("iteracja ",as.character(wykresy[[1]][2:5])),
       col=colors[2:5], lty=rep(1,4), cex=0.8)


