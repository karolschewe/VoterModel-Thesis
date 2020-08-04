this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)


processFile = function(filepath) {
  con = file(filepath, "r")
  line = readLines(con, n = 1)
  line.vec<-sub("\\[","(",line)
  line.vec<-sub("\\]",")",line.vec)
  line.vec<-paste0("c",line.vec)
  true.vec<- eval(parse(text = line.vec))

  
  close(con)
  return(true.vec)
}

# seqq<-seq(0.01,0.11,by = 0.01)

# par(mfrow=c(3,3))
par(mfrow=c(1,3))
seqq<- 0.02
d_factor<-38
for(i in seqq )
{
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/opinions_",i,".txt"))
  # print(first.timeseries)
  hist(first.timeseries, main = paste0("opinions in model D = ", i,"\n factor = ", d_factor),breaks = 25, xlab = 'CONSERVATISM SUPPORT')
}
for(i in seqq)
{
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/d_",i,"_sdev.txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("std. deviation in time D = ", i,"\n factor = ", d_factor), xlab = 'SYNCHRONOUS MODEL TIMESTEPS',ylab="sigma")
}


for(i in seqq)
{
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/mean_overall_",i,".txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("mean opinion in Poland in time D = ", i,"\n factor = ", d_factor), xlab = 'SYNCHRONOUS MODEL TIMESTEPS',ylab="sigma")
}



