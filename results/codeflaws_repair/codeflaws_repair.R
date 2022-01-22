knitr::opts_chunk$set(echo = TRUE)


library(ggplot2)
library(scales)
theme_set(theme_bw())


#Patch Quality
patch_quality=data.frame("subject"=character(),"category"=character(),"variable"=character(),"value"=numeric())

d=read.table("results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean(d,"Results_repair")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_repair.Rda")
  knit_exit()
}



#Repairability
for(i in 1:32){
  m_repair=0
  a_repair=0
  
  for(Subject in levels(factor(d$V1)))
  {
    specific=subset(d,V1==Subject & V2==i)
    if ("REPAIR" %in% specific$V11) m_repair=m_repair+1
    if ("REPAIR" %in% specific$V17) a_repair=a_repair+1
  }
  n_subjects=length(levels(factor(d$V1)))
  
  patch_quality <- rbind(patch_quality,data.frame(subject=Subject,category="Repairability",variable="Manual",value=m_repair/n_subjects))
  patch_quality <- rbind(patch_quality,data.frame(subject=Subject,category="Repairability",variable="Autogen",value=a_repair/n_subjects))
}


d_manual=subset(d,V11=="REPAIR")
d_autogen=subset(d,V17=="REPAIR")

patch_quality_1=data.frame(subject=d_manual$V1,
                           category=rep("Validation Score",nrow(d_manual)),
                           variable=rep("Manual",nrow(d_manual)),
                           value=d_manual$V13/d_manual$V14)

patch_quality_1=rbind(patch_quality_1,
                      data.frame(subject=d_autogen$V1,
                                 category=rep("Validation Score",nrow(d_autogen)),
                                 variable=rep("Autogen",nrow(d_autogen)),
                                 value=d_autogen$V19/d_autogen$V20))


patch_quality_1$variable<-factor(patch_quality_1$variable,levels=c("Manual","Autogen"),ordered=TRUE)



ggplot(patch_quality,aes(variable,value))+
  geom_violin(aes(fill=variable),scale="width")+
  geom_boxplot(width=0.1,outlier.shape = NA)+
  scale_y_continuous(labels = scales::percent,limits =c(0,1))+
  facet_grid(~ category)+
  xlab("Test suite")+ylab("%Subjects Repaired")+
  scale_fill_grey(start = 0.6,end=0.9)+
  theme(legend.position = "none", legend.title = element_blank(),
        axis.text.x = element_text(colour = "black"),axis.text.y = element_text(colour = "black"))
ggsave(filename = "Repairbility_violin.pdf",scale = 0.45,height=6)


ggplot(patch_quality_1,aes(variable,value))+
  geom_violin(aes(fill=variable),scale="width")+
  geom_boxplot(width=0.1,outlier.shape = NA)+
  scale_y_continuous(labels = scales::percent,limits =c(0,1))+
  facet_grid(~ category)+
  xlab("Test suite")+ylab("%Heldout test cases passed")+
  scale_fill_grey(start = 0.6,end=0.9)+
  theme(legend.position = "none", legend.title = element_blank(),
        axis.text.x = element_text(colour = "black"),axis.text.y = element_text(colour = "black"))

ggsave(filename = "patch_quality_individual_violin.pdf",scale = 0.45,height=6)


print(paste("Average/Median repairabiilty manual: ",mean(subset(patch_quality,variable=="Manual")$value,na.rm=TRUE),median(subset(patch_quality,variable=="Manual")$value,na.rm=TRUE)))
print(paste("Average/Median repairabiilty autogen: ",mean(subset(patch_quality,variable=="Autogen")$value,na.rm=TRUE),median(subset(patch_quality,variable=="Autogen")$value,na.rm=TRUE)))
print(paste("Average/Median Passing manual validation score: ", mean(subset(patch_quality_1, variable == "Manual")$value,na.rm =TRUE),median(subset(patch_quality_1,variable == "Manual")$value,na.rm =TRUE)))
print(paste("Average/Median Passing autogen validation score: ", mean(subset(patch_quality_1, variable == "Autogen")$value,na.rm =TRUE),median(subset(patch_quality_1,variable == "Autogen")$value,na.rm =TRUE)))


