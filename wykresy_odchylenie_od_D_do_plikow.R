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

seqq<- c(0,0.01,0.02,0.03,0.04,0.05,0.1,0.15,0.2,0.25)
d_factor<-38
folder<-"2020-08-17"

for(i in seqq )
{
  dir.create(file.path(this.dir, folder),showWarnings = F)
  png(paste0(folder,"/fact_",d_factor,"_d_",i,".png"),width = 600,height = 600)
  par(mfrow=c(2,2))
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/opinions_",i,".txt"))
  # print(first.timeseries)
  hist(first.timeseries, main = paste0("opinions in model D = ", i,"\n factor = ", d_factor),breaks = 25, xlab = 'CONSERVATISM SUPPORT')
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/d_",i,"_sdev.txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("std. deviation in time D = ", i,"\n factor = ", d_factor), xlab = 'SYNCHRONOUS MODEL TIMESTEPS',ylab="sigma")
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/mean_overall_",i,".txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("mean opinion in Poland in time D = ", i,"\n factor = ", d_factor), xlab = 'SYNCHRONOUS MODEL TIMESTEPS',ylab="mean")
  first.timeseries<-processFile(paste0("data/d_",i,"_scale_",d_factor,"/means_",i,".txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("mean opinion in Poland in time D = ", i,"\n on gmina level factor = ", d_factor), xlab = 'SYNCHRONOUS MODEL TIMESTEPS',ylab="mean")
  dev.off()
}

