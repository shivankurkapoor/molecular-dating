library(lme4)
plot(diversity~time, data = dataset3,  pch = c(1, 2, 3,4,5,6,7,8)[as.numeric(subject)])
linmod = lm(diversity~time  + I(time^2), data = dataset3)
lines(seq(0,800,by=10), predict(linmod, newdata = data.frame(time = seq(0,800,by=10))),col = 'red')
mixmod = lmer(diversity~time  + I(time^2) + (time  + I(time^2)|subject), data = dataset3);
for(i in 1:8)
  lines(seq(0,800,by=10), predict(mixmod, newdata = data.frame(time = seq(0,800,by=10),subject = rep(i,81))),col = 'green');
coef(mixmod);
coef(linmod)