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
oracle_quality = data.frame("subject"=character(),"gen_level"=character(),"variable"=character(), "value"=numeric())
#Labelling effort
labelling_effort= data.frame("subject"=character(),"gen_level"=character(),"variable"=character(),"number"=numeric())

# No generalize

d=read.table("GI/results_introclass.csv",sep=",",comment.char ="#")
mean_data=compute_mean_introclass(d,"Results_introclass_GI")
 
if(length(levels(factor(mean_data$main_sub)))!=length(levels(factor(d$V1))))
{
   print("DELETE Results_introclass_GI.Rda")
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
 
       oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="GI",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
       oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="GI",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
       oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="GI",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
 
       labelling_effort <- rbind(labelling_effort,data.frame(subject=tmp_sub_name,gen_level="GI",variable="No. Labels",number=sp_ins$n_labelled))
     }
   }
 }
 
 d=read.table("GI/results_quixbugs.csv",sep=",",comment.char ="#")
 mean_data=compute_mean_quixbugs(d,"Results_quixbugs_GI")
 
 if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
 {
   print("DELETE Results_quixbugs_GI.Rda")
   knit_exit()
 }
 
 for(Subject in levels(factor(mean_data$subject)))
 {
 
   sp_ins=subset(mean_data,subject==Subject)
 
   oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GI",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
   oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GI",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
   oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GI",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
   labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="GI",variable="No. Labels",number=sp_ins$n_labelled))
 
 }
 
 d=read.table("GI/results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean_codeflaws(d,"Results_codeflaws_GI")
 
  if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
  {
    print("DELETE Results_codeflaws_GI.Rda")
    knit_exit()
  }
 
 for(Subject in levels(factor(mean_data$subject)))
  {
 
    sp_ins=subset(mean_data,subject==Subject)
 
    oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GI",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
    oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GI",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
    oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GI",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
    labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="GI",variable="No. Labels",number=sp_ins$n_labelled))
 
 }



#Generalization 1

d=read.table("BG/results_introclass.csv",sep=",",comment.char ="#")
mean_data=compute_mean_introclass(d,"Results_introclass_BG")

if(length(levels(factor(mean_data$main_sub)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_introclass_BG.Rda")
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

      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="BG",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="BG",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="BG",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))

      labelling_effort <- rbind(labelling_effort,data.frame(subject=tmp_sub_name,gen_level="BG",variable="No. Labels",number=sp_ins$n_labelled))
    }
  }
}

d=read.table("BG/results_quixbugs.csv",sep=",",comment.char ="#")
mean_data=compute_mean_quixbugs(d,"Results_quixbugs_BG")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_quixbugs_BG.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="BG",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="BG",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="BG",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="BG",variable="No. Labels",number=sp_ins$n_labelled))

}

d=read.table("BG/results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean_codeflaws(d,"Results_codeflaws_BG")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_codeflaws_BG.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="BG",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="BG",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="BG",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="BG",variable="No. Labels",number=sp_ins$n_labelled))

}
# 
# Generalizatino 1-2


d=read.table("HSC/results_introclass.csv",sep=",",comment.char ="#")
mean_data=compute_mean_introclass(d,"Results_introclass_HSC")

if(length(levels(factor(mean_data$main_sub)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_introclass_HSC.Rda")
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

      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="HSC",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="HSC",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="HSC",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))

      labelling_effort <- rbind(labelling_effort,data.frame(subject=tmp_sub_name,gen_level="HSC",variable="No. Labels",number=sp_ins$n_labelled))
    }
  }
}

d=read.table("HSC/results_quixbugs.csv",sep=",",comment.char ="#")
mean_data=compute_mean_quixbugs(d,"Results_quixbugs_HSC")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_quixbugs_HSC.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="HSC",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="HSC",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="HSC",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="HSC",variable="No. Labels",number=sp_ins$n_labelled))

}


d=read.table("HSC/results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean_codeflaws(d,"Results_codeflaws_HSC")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_codeflaws_HSC.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="HSC",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="HSC",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="HSC",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="HSC",variable="No. Labels",number=sp_ins$n_labelled))

}

# Generalization 1-3

d=read.table("CCF/results_introclass.csv",sep=",",comment.char ="#")
mean_data=compute_mean_introclass(d,"Results_introclass_CCF")

if(length(levels(factor(mean_data$main_sub)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_introclass_CCF.Rda")
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

      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="CCF",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="CCF",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="CCF",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))

      labelling_effort <- rbind(labelling_effort,data.frame(subject=tmp_sub_name,gen_level="CCF",variable="No. Labels",number=sp_ins$n_labelled))
    }
  }
}


d=read.table("CCF/results_quixbugs.csv",sep=",",comment.char ="#")
mean_data=compute_mean_quixbugs(d,"Results_quixbugs_CCF")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_quixbugs_CCF.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="CCF",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="CCF",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="CCF",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="CCF",variable="No. Labels",number=sp_ins$n_labelled))

}

d=read.table("CCF/results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean_codeflaws(d,"Results_codeflaws_CCF")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_codeflaws_CCF.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="CCF",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="CCF",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="CCF",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="CCF",variable="No. Labels",number=sp_ins$n_labelled))

}

# Extension

d=read.table("GE/results_introclass.csv",sep=",",comment.char ="#")
mean_data=compute_mean_introclass(d,"Results_introclass_GE.Rda")

if(length(levels(factor(mean_data$main_sub)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_introclass_GE.Rda")
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

      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="GE",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="GE",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
      oracle_quality <- rbind(oracle_quality,data.frame(subject=tmp_sub_name,gen_level="GE",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))

      labelling_effort <- rbind(labelling_effort,data.frame(subject=tmp_sub_name,gen_level="GE",variable="No. Labels",number=sp_ins$n_labelled))
    }
  }
 }

d=read.table("GE/results_quixbugs.csv",sep=",",comment.char ="#")
mean_data=compute_mean_quixbugs(d,"Results_quixbugs_GE")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_quixbugs_GE.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GE",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GE",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GE",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="GE",variable="No. Labels",number=sp_ins$n_labelled))

}

d=read.table("GE/results_codeflaws.csv",sep=",",comment.char ="#")
mean_data=compute_mean_codeflaws(d,"Results_codeflaws_GE")

if(length(levels(factor(mean_data$subject)))!=length(levels(factor(d$V1))))
{
  print("DELETE Results_codeflaws_GE.Rda")
  knit_exit()
}

for(Subject in levels(factor(mean_data$subject)))
{

  sp_ins=subset(mean_data,subject==Subject)

  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GE",variable="Overall", value=sp_ins$correct_v/sp_ins$total_v))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GE",variable="Failing", value=sp_ins$correct_v_fail/sp_ins$total_v_fail))
  oracle_quality <- rbind(oracle_quality,data.frame(subject=Subject,gen_level="GE",variable="Passing", value=sp_ins$correct_v_pass/sp_ins$total_v_pass))
  labelling_effort <- rbind(labelling_effort,data.frame(subject=Subject,gen_level="GE",variable="No. Labels",number=sp_ins$n_labelled))
}




ggplot(oracle_quality, aes(gen_level,value)) +
  geom_violin(aes(fill=variable),na.rm = TRUE,scale="width") +
  geom_boxplot(width=0.1,outlier.shape = NA)+
  scale_y_continuous(labels = scales::percent) +
  facet_grid(~ variable)+
  xlab("Generalization steps and extension") + ylab("Prediction Accuracy") +
  scale_fill_grey(start = 0.6, end = .9) +
  theme(legend.position="none", legend.title= element_blank(),axis.title = element_text(size=14),
        axis.text.x = element_text(colour = "black",size=12), axis.text.y = element_text(colour = "black",size=12))
ggsave(filename = "Accuracy_all_benchmarks_gen_wise_violin_plots.pdf", width=14)



ggplot(labelling_effort, aes(gen_level, number)) +
  geom_violin(aes(fill=variable),scale="width") +
  geom_boxplot(width=0.1,outlier.shape = NA)+
  scale_y_continuous(labels = waiver()) +
  xlab("Generalization steps and extension") + ylab("Number of Queries") +
  scale_fill_grey(start = 0.6, end = .9) +
  theme(legend.position="none", legend.title= element_blank(),axis.title = element_text(size=10),
        axis.text.x = element_text(colour = "black",size=10), axis.text.y = element_text(colour = "black",size=10))
ggsave(filename = "Labelling_effort_all_gen_wise_violin_plots.pdf",height = 5,scale=0.7)

ggplot(labelling_effort, aes(gen_level, number)) +
  geom_violin(aes(fill=variable),scale="width") +
  geom_boxplot(width=0.1,outlier.shape = NA)+
  scale_y_continuous(labels = waiver(),trans="log10") +
  xlab("Generalization steps and extension") + ylab("Number of Queries (log10)") +
  scale_fill_grey(start = 0.6, end = .9) +
  theme(legend.position="none", legend.title= element_blank(),axis.title = element_text(size=10),
        axis.text.x = element_text(colour = "black",size=10), axis.text.y = element_text(colour = "black",size=10))
ggsave(filename = "Labelling_effort_all_gen_wise_violin_plots_log_scale.pdf",height = 5,scale=0.7)


print(paste("GI-Average/Median Overall Prediction Accuracy :",mean(subset(oracle_quality,gen_level=="GI" & variable=="Overall")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="GI" & variable=="Overall")$value,na.rm = TRUE)))
print(paste("GI-Average/Median Failing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="GI" & variable=="Failing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="GI" & variable=="Failing")$value,na.rm = TRUE)))
print(paste("GI-Average/Median Passing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="GI" & variable=="Passing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="GI" & variable=="Passing")$value,na.rm = TRUE)))
print(paste("GI-Average/Median Labelling Effort :",mean(subset(labelling_effort,gen_level=="GI" & variable=="No. Labels")$number,na.rm=TRUE),median(subset(labelling_effort,gen_level=="GI" & variable=="No. Labels")$number,na.rm = TRUE)))

print(paste("BG-Average/Median Overall Prediction Accuracy :",mean(subset(oracle_quality,gen_level=="BG" & variable=="Overall")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="BG" & variable=="Overall")$value,na.rm = TRUE)))
print(paste("BG-Average/Median Failing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="BG" & variable=="Failing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="BG" & variable=="Failing")$value,na.rm = TRUE)))
print(paste("BG-Average/Median Passing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="BG" & variable=="Passing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="BG" & variable=="Passing")$value,na.rm = TRUE)))
print(paste("BG-Average/Median Labelling Effort :",mean(subset(labelling_effort,gen_level=="BG" & variable=="No. Labels")$number,na.rm=TRUE),median(subset(labelling_effort,gen_level=="BG" & variable=="No. Labels")$number,na.rm = TRUE)))

print(paste("HSC-Average/Median Overall Prediction Accuracy :",mean(subset(oracle_quality,gen_level=="HSC" & variable=="Overall")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="HSC" & variable=="Overall")$value,na.rm = TRUE)))
print(paste("HSC-Average/Median Failing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="HSC" & variable=="Failing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="HSC" & variable=="Failing")$value,na.rm = TRUE)))
print(paste("HSC-Average/Median Passing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="HSC" & variable=="Passing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="HSC" & variable=="Passing")$value,na.rm = TRUE)))
print(paste("HSC-Average/Median Labelling Effort :",mean(subset(labelling_effort,gen_level=="HSC" & variable=="No. Labels")$number,na.rm=TRUE),median(subset(labelling_effort,gen_level=="HSC" & variable=="No. Labels")$number,na.rm = TRUE)))

print(paste("CCF-Average/Median Overall Prediction Accuracy :",mean(subset(oracle_quality,gen_level=="CCF" & variable=="Overall")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="CCF" & variable=="Overall")$value,na.rm = TRUE)))
print(paste("CCF-Average/Median Failing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="CCF" & variable=="Failing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="CCF" & variable=="Failing")$value,na.rm = TRUE)))
print(paste("CCF-Average/Median Passing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="CCF" & variable=="Passing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="CCF" & variable=="Passing")$value,na.rm = TRUE)))
print(paste("CCF-Average/Median Labelling Effort :",mean(subset(labelling_effort,gen_level=="CCF" & variable=="No. Labels")$number,na.rm=TRUE),median(subset(labelling_effort,gen_level=="CCF" & variable=="No. Labels")$number,na.rm = TRUE)))

print(paste("GE-Average/Median Overall Prediction Accuracy :",mean(subset(oracle_quality,gen_level=="GE" & variable=="Overall")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="GE" & variable=="Overall")$value,na.rm = TRUE)))
print(paste("GE-Average/Median Failing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="GE" & variable=="Failing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="GE" & variable=="Failing")$value,na.rm = TRUE)))
print(paste("GE-Average/Median Passing Conditional Accuracy :",mean(subset(oracle_quality,gen_level=="GE" & variable=="Passing")$value,na.rm=TRUE),median(subset(oracle_quality,gen_level=="GE" & variable=="Passing")$value,na.rm = TRUE)))
print(paste("GE-Average/Median Labelling Effort :",mean(subset(labelling_effort,gen_level=="GE" & variable=="No. Labels")$number,na.rm=TRUE),median(subset(labelling_effort,gen_level=="GE" & variable=="No. Labels")$number,na.rm = TRUE)))
