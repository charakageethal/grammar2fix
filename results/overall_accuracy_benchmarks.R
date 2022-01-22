knitr::opts_chunk$set(echo = TRUE)


library(ggplot2)
library(scales)
theme_set(theme_bw())

compute_mean_codeflaws=function(data,filename){
  filename=paste(filename,".Rda",sep="")
  
  if(file.exists(filename))
  {
    load(filename)
    return(mean_data)
  }
  
  mean_data=data.frame("subject"=character(),"total_v"=numeric(),"correct_v"=numeric(),"total_v_fail"=numeric(),"correct_v_fail"=numeric(),"total_v_pass"=numeric(),"correct_v_pass"=numeric(),"n_labelled"=numeric())
  
  for(Subject in levels(factor(data$V1)))
  {
    
    total_v=0
    correct_v=0
    total_v_fail=0
    correct_v_fail=0
    total_v_pass=0
    correct_v_pass=0
    totalnLabelled=0
    Runs=0
    
    for(run in levels(factor(subset(data,V1==Subject)$V2)))
    {
      specific_run=subset(data,V1==Subject & V2==run)
      
      if(nrow(specific_run)!=0)
      {
        Runs=Runs+1
        total_v=total_v+specific_run$V3
        correct_v=correct_v+specific_run$V4
        total_v_fail=total_v_fail+specific_run$V5
        correct_v_fail=correct_v_fail+specific_run$V6
        total_v_pass=total_v_pass+specific_run$V7
        correct_v_pass=correct_v_pass+specific_run$V8
        totalnLabelled=totalnLabelled+specific_run$V9
      }
      
    }
    
    mean_data <- rbind(mean_data,data.frame(subject=Subject,
                                            total_v=total_v/Runs,
                                            correct_v=correct_v/Runs,
                                            total_v_fail=total_v_fail/Runs,
                                            correct_v_fail=correct_v_fail/Runs,
                                            total_v_pass=total_v_pass/Runs,
                                            correct_v_pass=correct_v_pass/Runs,
                                            n_labelled=totalnLabelled/Runs
    ))
    
    
    
  }
  
  save(mean_data,file=filename)
  return(mean_data)
  
}



compute_mean_introclass=function(data,filename){
  filename=paste(filename,".Rda",sep="")
  
  if(file.exists(filename))
  {
    load(filename)
    return(mean_data)
  }
  
  mean_data=data.frame("main_sub"=character(),"subject"=character(),"version"=character(),"total_v"=numeric(),"correct_v"=numeric(),"total_v_fail"=numeric(),"correct_v_fail"=numeric(),"total_v_pass"=numeric(),"correct_v_pass"=numeric(),"n_labelled"=numeric())
  
  for(m_sub in levels(factor(data$V1)))
  {
    for(Subject in levels(factor(subset(data,V1==m_sub)$V2)))
    {
      for(ver in levels(factor(subset(data,V1==m_sub & V2==Subject)$V3)))
      {
        total_v=0
        correct_v=0
        total_v_fail=0
        correct_v_fail=0
        total_v_pass=0
        correct_v_pass=0
        totalnLabelled=0
        Runs=0
        
        for(run in levels(factor(subset(data,V1==m_sub & V2==Subject & V3==ver)$V4)))
        {
          specific_run=subset(data,V1==m_sub & V2==Subject & V3==ver & V4==run)
          
          if(nrow(specific_run)!=0)
          {
            Runs=Runs+1
            total_v=total_v+specific_run$V5
            correct_v=correct_v+specific_run$V6
            total_v_fail=total_v_fail+specific_run$V7
            correct_v_fail=correct_v_fail+specific_run$V8
            total_v_pass=total_v_pass+specific_run$V9
            correct_v_pass=correct_v_pass+specific_run$V10
            totalnLabelled=totalnLabelled+specific_run$V11
          }
          
        }
        
        mean_data <- rbind(mean_data,data.frame(main_sub=m_sub,
                                                subject=Subject,
                                                version=ver,
                                                total_v=total_v/Runs,
                                                correct_v=correct_v/Runs,
                                                total_v_fail=total_v_fail/Runs,
                                                correct_v_fail=correct_v_fail/Runs,
                                                total_v_pass=total_v_pass/Runs,
                                                correct_v_pass=correct_v_pass/Runs,
                                                n_labelled=totalnLabelled/Runs
        ))
        
      }
      
    } 
  }
  
  
  
  save(mean_data,file=filename)
  return(mean_data)
  
}


compute_mean_quixbugs=function(data,filename){
  filename=paste(filename,".Rda",sep="")
  
  if(file.exists(filename))
  {
    load(filename)
    return(mean_data)
  }
  
  mean_data=data.frame("subject"=character(),"total_v"=numeric(),"correct_v"=numeric(),"total_v_fail"=numeric(),"correct_v_fail"=numeric(),"total_v_pass"=numeric(),"correct_v_pass"=numeric(),"n_labelled"=numeric())
  
  for(Subject in levels(factor(data$V1)))
  {
    
    total_v=0
    correct_v=0
    total_v_fail=0
    correct_v_fail=0
    total_v_pass=0
    correct_v_pass=0
    totalnLabelled=0
    Runs=0
    
    for(run in levels(factor(subset(data,V1==Subject)$V2)))
    {
      specific_run=subset(data,V1==Subject & V2==run)
      
      if(nrow(specific_run)!=0)
      {
        Runs=Runs+1
        total_v=total_v+specific_run$V3
        correct_v=correct_v+specific_run$V4
        total_v_fail=total_v_fail+specific_run$V5
        correct_v_fail=correct_v_fail+specific_run$V6
        total_v_pass=total_v_pass+specific_run$V7
        correct_v_pass=correct_v_pass+specific_run$V8
        totalnLabelled=totalnLabelled+specific_run$V9
      }
      
    }
    
    mean_data <- rbind(mean_data,data.frame(subject=Subject,
                                            total_v=total_v/Runs,
                                            correct_v=correct_v/Runs,
                                            total_v_fail=total_v_fail/Runs,
                                            correct_v_fail=correct_v_fail/Runs,
                                            total_v_pass=total_v_pass/Runs,
                                            correct_v_pass=correct_v_pass/Runs,
                                            n_labelled=totalnLabelled/Runs
    ))
    
    
    
  }
  
  save(mean_data,file=filename)
  return(mean_data)
  
}


#Oracle Quality
oracle_quality = data.frame("subject"=character(),"benchmark"=character(),"variable"=character(), "value"=numeric())
#Labelling effort
labelling_effort= data.frame("subject"=character(),"benchmark"=character(),"variable"=character(),"number"=numeric())


d=read.table("GE/results_introclass.csv",sep=",",comment.char ="#")
mean_data=compute_mean_introclass(d,"Results_introclass")

if(length(levels(factor(mean_data$main_sub)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_introclass.Rda")
  knit_exit()
}

for(m_sub in levels(factor(mean_data$main_sub))){
  
  for(Subject in levels(factor(subset(mean_data,main_sub==m_sub)$subject)))
  {
    for(ver in levels(factor(subset(mean_data,main_sub==m_sub & subject==Subject)$version)))
    {
      sp_ins=subset(mean_data,main_sub==m_sub & subject==Subject & version==ver)
      
      #sp_ins=subset(sp_ins,sp_ins$total_v_pass > 0)
      
      tmp_sub_name=paste(m_sub,Subject,ver,sep="_")
      
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,benchmark="IntroClass",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,benchmark="IntroClass",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,benchmark="IntroClass",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
      
      labelling_effort <- rbind(labelling_effort,data.frame(subject=tmp_sub_name,benchmark="IntroClass",variable="No. Labels",number=sp_ins$n_labelled))
    }
  }
}

d=read.table("GE/results_quixbugs.csv",sep=",",comment.char ="#")
mean_data=compute_mean_quixbugs(d,"Results_quixbugs")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_quixbugs.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{
  
  sp_ins=subset(mean_data,subject==Subject)
  
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,benchmark="QuixBugs",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,benchmark="QuixBugs",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,benchmark="QuixBugs",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,benchmark="QuixBugs",variable="No. Labels",number=sp_ins$n_labelled))
  
}


d=read.table("GE/results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean_codeflaws(d,"Results_codeflaws")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_codeflaws.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{
  
  sp_ins=subset(mean_data,subject==Subject)
  
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,benchmark="Codeflaws",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,benchmark="Codeflaws",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,benchmark="Codeflaws",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,benchmark="Codeflaws",variable="No. Labels",number=sp_ins$n_labelled))
  
}


ggplot(oracle_quality, aes(variable, value)) +
  geom_violin(aes(fill=variable),na.rm = TRUE,scale = "width") +
  geom_boxplot(width=0.1,outlier.shape = NA) +
  scale_y_continuous(labels = scales::percent) +
  xlab("") + ylab("Prediction Accuracy") +
  scale_fill_grey(start = 0.6, end = .9) +
  theme(legend.position="none", legend.title= element_blank(),
        axis.text.x = element_text(colour = "black"), axis.text.y = element_text(colour = "black"))
ggsave(filename = "Overall_accuracy_benchmarks.pdf", width=8,height=4.2,scale=0.77)

# ggplot(labelling_effort, aes(variable, number)) +
#   geom_violin(aes(fill=variable),scale = "width") +
#   geom_boxplot(width=0.1,outlier.shape = NA)+
#   scale_y_continuous(labels = waiver()) +
#   xlab("") + ylab("Number of queries") +
#   scale_fill_grey(start = 0.6, end = .9) +
#   theme(legend.position="none", legend.title= element_blank(),
#         axis.text.x = element_text(colour = "black"), axis.text.y = element_text(colour = "black"))
# ggsave(filename = "Labelling_effort_all_gen_1_4_violin.pdf", width=5,height=4.2,scale=0.77)

print(paste("Average/Median predication accuracy",mean(subset(oracle_quality,variable=="Overall")$value),median(subset(oracle_quality,variable=="Overall")$value)))

print(paste("Average/Median failing conditional accuracy",mean(subset(oracle_quality,variable=="Failing")$value),median(subset(oracle_quality,variable=="Failing")$value)))

print(paste("Average/Median passing conditional accuracy",mean(subset(oracle_quality,variable=="Passing")$value,na.rm=TRUE),median(subset(oracle_quality,variable=="Passing")$value,na.rm = TRUE)))

print(paste("Average/Median failing labelling effort",mean(subset(labelling_effort,variable=="No. Labels")$number),median(subset(labelling_effort,variable=="No. Labels")$number)))