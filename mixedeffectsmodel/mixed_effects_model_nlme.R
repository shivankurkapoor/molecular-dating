library(nlme)
library(data.table)
output_path = "/Users/shivankurkapoor/Desktop/Bioinfo/MixedEffectsModel/OUTPUT"
input_path = "/Users/shivankurkapoor/Desktop/Bioinfo/MixedEffectsModel/INPUT"

get_subject_name <- function(string, sep = "."){
  name <- strsplit(string, sep, fixed = TRUE)[[1]][1] 
  return (name)
}

load_data <- function(path){
  dir <- path
  file_paths <- list.files(dir, pattern="*.dat", full.names=TRUE)
  file_names <- list.files(dir, pattern="*.dat", full.names=FALSE)
  subject_names = lapply(file_names, get_subject_name)
  temp <- lapply(file_paths, fread, sep=" ")
  for(i in 1:length(temp)){
    temp[[i]][,"v3"] <- rep(as.factor(subject_names[[i]]), dim(temp[[i]])[1])
  }
  dataset <- rbindlist( temp )
  colnames(dataset) <- c("time", "diversity","subject")
  return (dataset)
}



mem_long_span <- function(dataset, path , days = 800){
 # png(file = paste(path,"mem_long_span.png",sep="/"))
  plot(diversity~time,
       xlab = 'Time',
       ylab = 'Diversity',
       pch = c(seq(1,length(levels(dataset$subject))[1]))[as.numeric(dataset$subject)],
       main = 'Mixed Effects Model',
       data = dataset)
  linmod = lm(diversity~time + I(time^2) + 0, data=dataset)
  lines(seq(0,days, by=10), predict(linmod, newdata=data.frame(time=seq(0,days,by=10))), col='red')
  mixmod = lme(diversity~time + I(time^2) +  0 , random = ~ time + I(time^2) + 0 | subject, data = dataset)
  for(i in 1:length(levels(dataset$subject)))
    lines(seq(0,days, by=10), predict(mixmod, newdata=data.frame(time=seq(0,days,by=10), subject = rep(levels(dataset$subject)[i],(days/10)+1))), col='blue')
  #dev.off()
  
  sum_file_name = paste("summary",toString(days),sep = "_")
  sum_file_name = paste(sum_file_name,"txt",sep = ".")
  sum_file_path <- paste(path,sum_file_name,sep="/")
  
  
  out <- capture.output(summary(mixmod))
  cat("##########################################  SUMMARY OF MIXED EFECTS MODEL FOR 800 DAYS #######################################", out, file=sum_file_path, sep="\n")
  out <- capture.output(coef(mixmod))
  cat("#################################  COEFFICIENTS FOR DIFFERENT SUBJECT  ###############################", out, file=sum_file_path, sep="\n", append=TRUE)
  out <- capture.output(summary(linmod))
  cat("##########################################  SUMMARY FOR THE LINEAR MODEL  #######################################", out, file=sum_file_path, sep="\n", append=TRUE)
  
  }

mem_short_span <- function(dataset,path, days = 150){
  
 # png(file = paste(path,"mem_short_span.png",sep="/"))
  dataset = dataset[dataset$time<=days,]
  plot(diversity~time,
       xlab = 'Time',
       ylab = 'Diversity',
       pch = c(seq(1,length(levels(dataset$subject))[1]))[as.numeric(dataset$subject)],
       main = 'Linear Model',
       data = dataset)
  subs = levels(dataset$subject)
  linmod = lm(diversity~time +0, data=dataset)
  lines(seq(0,days, by=10), predict(linmod, newdata=data.frame(time=seq(0,days,by=10))), col='red')
  mixmod = lme(diversity~time + 0 ,random = ~ time + 0 | subject, data = dataset)
  for(i in 1:length(levels(dataset$subject)))
    lines(seq(0,days, by=10), predict(mixmod, newdata=data.frame(time=seq(0,days,by=10), subject = rep(levels(dataset$subject)[i],(days/10)+1))), col='blue')
  
  #dev.off()

  sum_file_name = paste("summary",toString(days),sep = "_")
  sum_file_name = paste(sum_file_name,"txt",sep = ".")
  sum_file_path <- paste(path,sum_file_name,sep="/")
  
  out <- capture.output(summary(mixmod))
  cat("##################################  SUMMARY OF MIXED EFECTS MODEL FOR FIRST 150 DAYS #####################################", out, file=sum_file_path, sep="\n")
  out <- capture.output(coef(mixmod))
  cat("#################################  COEFFICIENTS FOR DIFFERENT SUBJECT  ###############################", out, file=sum_file_path, sep="\n", append=TRUE)
  out <- capture.output(summary(linmod))
  cat("################################# SUMMARY FOR THE LINEAR MODEL  #################################", out, file=sum_file_path, sep="\n", append=TRUE)
  
}

dataset <- load_data(input_path)
dataset = dataset[order(dataset$time)]
plot(diversity~time,
     xlab = 'Time',
     ylab = 'Diversity',
     pch = c(seq(1,length(levels(dataset$subject))[1]))[as.numeric(dataset$subject)],
     main = 'Diversity for different subjects',
     data = dataset)
fit <- lm(diversity~time+I(time^2)+0, data = dataset)
pred.int <- predict(fit,interval="prediction")
conf.int <-  predict(fit,interval="confidence")
fitted.values = pred.int[,1]
pred.lower = pred.int[,2]
pred.upper = pred.int[,3]
lines(dataset$time[1:71],fitted.values[1:71],col="red",lwd=2)
lines(dataset$time[1:71],pred.lower[1:71],lwd=2,col="blue")
lines(dataset$time[1:71],pred.upper[1:71],lwd=2,col="blue")
#mem_long_span(dataset = dataset, path = output_path)
#mem_short_span(dataset = dataset, path = output_path)
