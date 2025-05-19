
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%Linear model for WEC - Student version %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
clear all
% Sets constants and upload data 
    load wcylinder1_4_05, load wcylinder3_4_05                               % Load WAMIT, hydrodynamical coefficients                                 
    load Islandsberg_Wave_record                                             % Load Wave record (30 min time series, with sampling freq. 2.56 Hz)

    wave_amp  = (Islandsberg_Wave_record(:,1))*10^-2;                        % amplitude for incoming wave [m]
    wave_amp  = wave_amp - mean(wave_amp);                                   % fix the biased amplitude
    dt        = 1/2.56;                                                      % sampling f = 2.56 Hz
    wave_time = dt:dt:dt*4608;                                               % time vector for incoming wave [s]
                                                                                                   
    dw = .01;                                                                % default value for interpolation
    dt = .01;                                                                % default value for interpolation
    
    rho    = 1000;                                                            % water density [kg/m3]
    g      = 9.81;                                                            % gravity
    r      = 2;                                                               % buoy radius [m]
    A      = pi*r^2;                                                          % buoy area [m2]
    draft  = .5;                                                              % buoy draft (with no translator attached) [m]
    ks     = 4000;                                                            % spring constant [N/m]
    m      = (A*draft*rho)+1000;                                              % mass of buoy and piston/translator [kg]
    gamma  = 40000;                                                           % example of damping coefficient [Ns/m]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
% Sorting and scaling the data
    [T]        = wcylinder1_4_05(:,1);                                       % period
    [w]        = (2*pi)./T;                                                  % angular frequency
    [ma]       = wcylinder1_4_05(:,4);                                       % added mass
    [rr]       = wcylinder1_4_05(:,5);                                       % radiation resistance
    [absfe]    = wcylinder3_4_05(:,4);                                       % absolute value of excitation force
    [argfe]    = wcylinder3_4_05(:,5);                                       % argument of excitation force
    [ma]    = ma*rho;                                                        % scaling added mass
    [rr]    = rr*rho.*w;                                                     % scaling radiation resistance
    [absfe] = absfe*rho*g;                                                    % scaling the absolute value of the excitation force

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
% Calculate the excitation force
    [fe] = absfe.*cos(pi*argfe/180) + 1i*absfe.*sin(pi*argfe/180);            % excitation force
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
% Calculate the transfer function between wave and buoy amplitud, also
% called the Response Amplitude Operator (RAO)
    [H]    = fe./(-(w.^2) .*(m+ma) + 1i*w.*(gamma + rr) + rho*g*A + ks);     % RAO 
    [argH] = atan(imag(H)./real(H));                                         % argument of RAO         
    [argH] = argH*180/pi;                                                     % convert into degrees
    [absH] = abs(H);                                                          % absolute value of RAO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Adding zeros
    Nollor = zeros(100,1);
    HN     = [Nollor;flipud(real(H));real(H(1));real(H);Nollor]...
             + 1i*[Nollor;flipud(-imag(H));0;imag(H);Nollor];    
    dww    = abs(w(2)-w(1));                                                  
    N      = (length(HN)-1)/2;  
    wHN    = (-dww*N:dww:dww*N)';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Interpolate to increase the resolution    
    wH  = (dw:dw:max(wHN))';  
    wH  = [flipud(-wH);0;wH];
    H   = interp1(wHN,real(HN),wH,'spline')...
        + 1i*interp1(wHN,imag(HN),wH,'spline');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
           
% Calculate the invers fouriertransform 
    dtt   = 2*pi/(length(H)*dw);                                           
    [h]   = (1/dtt)*fftshift(ifft(fftshift(H)));
    [t]   = ((1:length(h))-(length(h)+1)/2)*(dtt);   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Speeding up 
    h = real(h);  MAX = abs(max(h)); eps = 0.005; flag = 0; index = 0;     
    while flag == 0
      index = index + 1;
      if abs(h(index))/MAX > eps
        flag = 1;
        index1 = index;
      end
    end
    index = length(h) + 1;  flag = 0;
    while flag == 0
      index = index - 1;
      if abs(h(index))/MAX > eps
        flag = 1;
        index2 = index;
      end
    end
    h = h(index1:index2);
    t = t(index1:index2);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

% Convolution between RAO and wave to get buoy position 
    thI    = min(t):dt:max(t);                                                 % time vector for RAO with increased resolution
    twaveI = min(wave_time):dt:max(wave_time);                                % time vector for wave with increased resolution
    
    hI     = interp1(t,h,thI,'spline');                                       % interpolating RAO
    WaveI  = interp1(wave_time,wave_amp,twaveI,'spline');                      % interpolating wave
    
    z      = conv(hI,WaveI)*dt;                                               % convolution function between RAO and wave
 
    MIN    = min(abs(thI));
    index  = find(abs(thI) == MIN);
    N1     = length(hI);
    N2     = length(z);
    z      = z(index:N2-(N1-index))';                                         % buoy vertical position in time domain [m]
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
