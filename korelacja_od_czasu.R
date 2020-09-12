library(circlize)


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

d_values<-c(0,0.01,0.02,0.03,0.06,0.1)
# d_values = [0,0.01,0.02,0.03,0.06,0.1]
# downscale_factors = [38,100]
for (d in d_values)
  {
  png(paste0("2020-09-12-onlywrk/zz_fac100_d_",d,".png"))
  wykresy<-processBigFile(paste0("data_new_corr_long_only_wrk/d_",d,"_scale_100noise_change/d_",d,"_corr_of_time.txt"))
  km<-c(10^1,10^1.2,10^1.4,10^1.6,10^1.8,10^2,10^2.2,10^2.4,10^2.6,10^2.8)
  vvv<-plot(y = wykresy[[2]][[1]],x = km, 
            main = paste0("korelacja od odleglosci factor = 100 d=",d), log = "x",ylab = "korelacja",ylim = c(-0.06,0.25))
  wartosci<-c()
  for (i in 2:length(wykresy[[1]]))
  {
    vvv<-vvv+lines(y = wykresy[[2]][[i]], x = km, col = rand_color(10,luminosity = "bright"), lty=(i%%3)*2+1)  
    wartosci<-rbind(wartosci,wykresy[[2]][[i]])
  }
  srednia<-colMeans(wartosci)
  vvv<-vvv+lines(y = srednia, x = km, lwd = 4)
  
  legend("bottomleft", legend=c("dane","usrednione z modelu"),
         pch = c(1,NA),lty = c(NA,1), lwd = c(NA,4), cex=0.8)
  dev.off()
  
  }





  


