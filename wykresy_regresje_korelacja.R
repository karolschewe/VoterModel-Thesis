this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)


seqq<- c(0.02,0)


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


d_factor<-38*1
df<-expand.grid(d = seqq,factor = d_factor, sigma = NA)


folder<-"2020-08-21"
noise<-"noise_change"
datacollected<-"do_wykresow_magisterka"


km<-c(10^1,10^1.2,10^1.4,10^1.6,10^1.8,10^2,10^2.2,10^2.4,10^2.6,10^2.8)
logkm<-seq(1,2.8,0.2)


for(jj in d_factor)
{
  par(mfrow=c(1,1))
  for(i in seqq)
  {
    korelacje<-processFile(paste0(datacollected,"/d_",i,"_scale_",jj,noise,"/spatial_correlation_",i,".txt"))
    reglin<-lm(korelacje ~ logkm)
    df$nachylenie[which(df$d==i & df$factor == jj)]<-reglin$coefficients[2]
    plot(x = km,y=korelacje, log = "x", main = paste0("korelacje od odleglosci dla\nd:",i," zmniejszenia:",jj))+lines(x = km,predict(reglin))
  }
}

