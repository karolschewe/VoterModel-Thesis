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

seqq<- "0.0001"
d_factor<-6

par(mfrow=c(2,2), mar = c(5, 4, 6, 2) + 0.1)
for(i in seqq )
{
  first.timeseries<-processFile(paste0("do_wykresow_magisterka_factors/d_",i,"_scale_",d_factor,"noise_change_a0.5/opinions_",i,".txt"))
  # print(first.timeseries)
  hist(first.timeseries, main = paste0("\n\n\n\nRozk³ad opinii\n po zakoñczeniu iteracji modelu"),breaks = 25, xlab = 'CONSERVATISM SUPPORT',cex.main = 1)
}
for(i in seqq)
{
  first.timeseries<-processFile(paste0("do_wykresow_magisterka_factors/d_",i,"_scale_",d_factor,"noise_change_a0.5/d_",i,"_sdev.txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("\n\n\n\nOdchylenie standardowe"), xlab = 'MODEL TIMESTEPS',ylab="sigma",cex.main = 1)
}


for(i in seqq)
{
  first.timeseries<-processFile(paste0("do_wykresow_magisterka_factors/d_",i,"_scale_",d_factor,"noise_change_a0.5/mean_overall_",i,".txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("\n\nProcentowe poparcie konserwatyzmu"), xlab = 'MODEL TIMESTEPS',ylab="mean",cex.main = 1)
}


for(i in seqq)
{
  first.timeseries<-processFile(paste0("do_wykresow_magisterka_factors/d_",i,"_scale_",d_factor,"noise_change_a0.5/means_",i,".txt"))
  # print(first.timeseries)
  plot(first.timeseries, main = paste0("\n\nŒrednie poparcie konserwatyzmu\n na poziomie gminy"), xlab = 'MODEL TIMESTEPS',ylab="mean",cex.main = 1)
}


title(paste0("W³aœciwoœci modelu dla parametrów\n D = ",seqq," alfa = 0.5, skala zminiejszenia 1:",d_factor), line = -3, outer = TRUE, cex.main = 1.4)
