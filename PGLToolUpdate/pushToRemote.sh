#!/bin/sh

#pull first
#git pull

#remove old ranking tables from local repo and local disk
#rm -rf /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/oras/*
#rm -rf /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/xy/*

#move new current ranking tables to local repo
#mv /home/ubuntu/PGLDataUpdate/CurrentSeason/oras/* /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/oras/
#mv /home/ubuntu/PGLDataUpdate/CurrentSeason/xy/* /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/xy/

#move new checkUdata.txt to local repo
#mv /home/ubuntu/PGLDataUpdate/CurrentSeason/checkUpdate.txt /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/

#move new past season to local repo
#cp -r /home/ubuntu/PGLDataUpdate/HistoryRepo/tempOras/* /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/history/oras/
#cp -r /home/ubuntu/PGLDataUpdate/HistoryRepo/tempXy/* /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/history/xy/

#move new historyList.txt to local repo
#cp -f /home/ubuntu/PGLDataUpdate/HistoryRepo/oras-historyList.txt /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/history/oras/
#cp -f /home/ubuntu/PGLDataUpdate/HistoryRepo/xy-historyList.txt /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest/history/xy/

#add,commit,push
git add -A /home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/DataTest
git commit -m 'Sylvia'
git push origin master

#move new past season to history 
mv /home/ubuntu/PGLDataUpdate/HistoryRepo/tempOras/* /home/ubuntu/PGLDataUpdate/HistoryRepo/oras
mv /home/ubuntu/PGLDataUpdate/HistoryRepo/tempXy/* /home/ubuntu/PGLDataUpdate/HistoryRepo/xy