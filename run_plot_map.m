load data;

last_no = 38;

h = figure; hold on; axis square; axis off;
plot(data(end-last_no:end,3),data(end-last_no:end,2),'r.','markersize',10);
%plot(data2(:,3),data2(:,2),'b.','markersize',10);
%plot_google_map('maptype','hybrid','AutoAxis',1,'Alpha',0.4);
%legend('raw','corr');
%print(h,'-dpng','-r256','fig_skrydis_raw.png');
%print(h,'-dpng','-r256','fig_skrydis_su_ir_be_kor.png');
%print(h,'-dpng','-r256','fig_skrydis_baigtis.png');

%baigtis 30 sec
%(data(end,1) - data(end-last_no,1))*60

lw = 3; fs = 14;
h = figure; hold on; 
set(gca,'fontsize',fs);
plot((data(end-last_no:end,1)-data(end-last_no,1))*60,data(end-last_no:end,4)*1000,'r-','linewidth',lw);
xlabel('time (s)');
ylabel('altitude (m)');
title('Last 30 sec');
print(h,'-dpng','-r256','fig_skrydis_aukstis.png');


p = polyfit((data(end-last_no+4:end,1)-data(end-last_no+4,1))*60,data(end-last_no+4:end,5),2);
y = polyval(p,(data(end-last_no+4:end,1)-data(end-last_no+4,1))*60);

lw = 3; fs = 14;
h = figure; hold on; 
set(gca,'fontsize',fs);
plot((data(end-last_no:end,1)-data(end-last_no,1))*60,data(end-last_no:end,5),'ko-','linewidth',lw-2);
plot((data(end-last_no+4:end,1)-data(end-last_no+4,1))*60+4,y,'b-','linewidth',lw);
legend('observed','fitted','Location','SouthEast');
xlabel('time (s)');
ylabel('vertical speed (m/s)');
title('Last 30 sec');
print(h,'-dpng','-r256','fig_skrydis_kritimo_greitis.png');

h = figure; hold on; 
set(gca,'fontsize',fs);
plot((data(end-last_no:end,1)-data(end-last_no,1))*60,data(end-last_no:end,6),'ko-','linewidth',lw-2);
xlabel('time (s)');
ylabel('ground speed (m/s)');
title('Last 30 sec');
print(h,'-dpng','-r256','fig_skrydis_horizontalus_greitis.png');
