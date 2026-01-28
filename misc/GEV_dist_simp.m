clc;
clear;

% # get maximum value for each year
T = table2array(readtable('station_output_mod.txt'));
hour = T(:,1);
discharge = T(:,10);
n_year = 30;
n_output_per_year = 365*4*n_year;
n_hour_oneYear = 365*4;
max_array = zeros(1,n_year);
for yr=1:n_year
    % range of interest
    discharge_selected = discharge((yr-1)*n_hour_oneYear+1:(yr)*n_hour_oneYear);
    max_array(yr) = max(discharge_selected);
    disp("Finished MAX for year "+string(yr))
end

% ## sort small to large 
data_ex1=sort(max_array); 
sample_mean=mean((data_ex1));
sample_std=std(data_ex1);
% Define the Gumbel distribution function
ex_alpha = sqrt(6) / pi * sample_std; % scale parameter;
ex_xi = sample_mean - (-psi(1)) * ex_alpha; % location parameter
% Given return period
T0 = 75; 
% Calculate the exceedance probability (F)
F_T0 = 1 - 1/T0;
% Calculate the corresponding y-value (y0) using the Gumbel distribution function
y0 = ex_xi + ex_alpha * (-log(-log(F_T0)));
figure(1);
hold on;
plot(-log(-log(F_T0)), y0, 'bx', 'MarkerSize', 10, 'LineWidth', 2); % Plot the point
text(-log(-log(F_T0)), y0, [' x = ', num2str(y0, '%.2f'), ' days'], 'VerticalAlignment', 'bottom', ...
    'HorizontalAlignment', 'right','Color', 'blue');
% T0 on the axis
xline(-log(-log(F_T0)),':k');
text(-log(-log(F_T0)),0.5,num2str(T0),'HorizontalAlignment','center') % y0 display