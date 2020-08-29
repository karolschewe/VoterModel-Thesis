this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
library(ggplot2)

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

seqq<- c(0,0.02,0.04,0.06,0.8,0.1,0.2)

d_factor<-38*1:4
df<-expand.grid(d = seqq,factor = d_factor, sigma = NA)


folder<-"2020-08-21"
noise<-"noise_change"
for(i in seqq )
{
  for(jj in d_factor)
  {
    first.timeseries<-processFile(paste0("data_corr/d_",i,"_scale_",jj,noise,"/d_",i,"_sdev.txt"))
    # print(first.timeseries)
    print(paste0("D:",i))
    bez_poczatku <- 30:length(first.timeseries)
    tmp<-mean(first.timeseries[bez_poczatku])
    print(tmp)
    df$sigma[which(df$d==i & df$factor == jj)]<-tmp
    
  }
  
  
}


v <- ggplot(df, aes(d, factor, z =sigma)) + 
  geom_raster(aes(fill = sigma)) + 
  ggtitle("Odchylenie standardowe rozkładu opinii w gminach\nod intesywności szumu i skali zmniejszenia układu\nuśrednione po stabilizacji układu (z 20 kroków czasowych)")

km<-c(10^1,10^1.2,10^1.4,10^1.6,10^1.8,10^2,10^2.2,10^2.4,10^2.6,10^2.8)
logkm<-seq(1,2.8,0.2)


for(i in seqq )
{
  for(jj in d_factor)
  {
    korelacje<-processFile(paste0("data_corr/d_",i,"_scale_",jj,noise,"/spatial_correlation_",i,".txt"))
    reglin<-lm(korelacje ~ logkm)
    df$nachylenie[which(df$d==i & df$factor == jj)]<-reglin$coefficients[2]
  }
}


v2 <- ggplot(df, aes(d, factor, z =nachylenie)) + 
  geom_raster(aes(fill = nachylenie)) +
  ggtitle("Nachylenie krzywej korelacji od odleglosci\nw zaleznosci od skali zmniejszenia i natezenia szumu")



