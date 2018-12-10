%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: demoGenerateTSMWebsite
% Date: 12-2013
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% This is a demo script which shows how the 'TSM toolbox' can be used to
% generate a website for comparing the TSM results of the various TSM
% algorithms included in the toolbox.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reference: 
% If you use the 'TSM toolbox' please refer to:
% [DM14] Jonathan Driedger, Meinard Mueller
%        TSM Toolbox: MATLAB Implementations of Time-Scale Modification 
%        Algorithms
%        Proceedings of the 17th International Conference on Digital Audio  
%        Effects, Erlangen, Germany, 2014.
%
% License:
% This file is part of 'TSM toolbox'.
% 
% 'TSM toolbox' is free software: you can redistribute it and/or modify it
% under the terms of the GNU General Public License as published by the
% the Free Software Foundation, either version 3 of the License, or (at
% your option) any later version.
% 
% 'TSM toolbox' is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
% Public License for more details.
% 
% You should have received a copy of the GNU General Public License along
% with 'TSM toolbox'. If not, see http://www.gnu.org/licenses/.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% initialization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
pathData = 'data/';                        % path to the source files
pathOutput = 'output/';
pathHtml = [pathOutput 'website/'];        % path to the website folder
nameTable = 'tables.html';
nameIndexTemplate = 'indexTemplate.html';
nameStyle = 'style.css';
nameFiles = {                              % files that should be processed
    'Bongo.wav';
    'CastanetsViolin.wav';
    'DrumSolo.wav';
    'Glockenspiel.wav';
    'Stepdad.wav';
    'Jazz.wav';
    'Pop.wav';
    'SingingVoice.wav';
    'SynthMono.wav';
    'SynthPoly.wav';
    };

stretchingFactors = [0.5 1.2 1.8];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% file handling
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% generate website directory
if ~isdir(pathHtml)
    mkdir(pathHtml)
end

% html index template
fid = fopen([pathData nameIndexTemplate],'r');
index_template = fread(fid, '*char')';
fclose( fid );

% html index file where the code for the table will be put in
index_out = fopen([ pathHtml 'index.html'], 'w');

% create the html file for the tables
hTables = fopen([pathHtml nameTable],'w+t');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% generate the tables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
warning('OFF','MATLAB:audiovideo:audiowrite:dataClipped');

for s = stretchingFactors
    disp(['Generating table and audio files for stretching factor ' ...
        num2str(s)]);
    
    % write title of the table
    fprintf(hTables,'<h3>Constant stretching factor of &alpha;=%s</h3>',...
        num2str(s));
    
    % write the head of the table
    fprintf(hTables,'<center>\n');
    fprintf(hTables, '<table>\n');
    
    % write the head row of the table
    fprintf(hTables, '<tr>\n');
    fprintf(hTables, '<th><b>Name</b></th>\n');
    fprintf(hTables, '<th><b>Original</b></th>\n');
    fprintf(hTables, '<th><b>OLA</b></th>\n');
    fprintf(hTables, '<th><b>WSOLA</b></th>\n');
    fprintf(hTables, '<th><b>Phase Vocoder</b></th>\n');
    fprintf(hTables, '<th><b>Phase Vocoder <br>(phase locking)</b></th>\n');
    fprintf(hTables, '<th><b>TSM based on <br>HPSS</b></th>\n');
    fprintf(hTables, '<th><b>&eacute;lastique</b></th>\n');
    fprintf(hTables, '</tr>\n');
    
    % separator line
    fprintf(hTables, '<tr align="center">\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '<th class="separator"></th>\n');
    fprintf(hTables, '</tr>\n');
    
    % iterate over all items
    for i = 1: length(nameFiles)
        name = nameFiles{i};
        disp(['  ' name]);
        
        % construct filenames
        name_ORIG = [name(1:end-4) '_ORIG.wav']; 
        name_OLA = [name(1:end-4) '_' sprintf('%0.2f',s) '_OLA.wav'];
        name_WSOLA = [name(1:end-4) '_' sprintf('%0.2f',s) '_WSOLA.wav'];
        name_PV = [name(1:end-4) '_' sprintf('%0.2f',s) '_PV.wav'];
        name_PVpl = [name(1:end-4) '_' sprintf('%0.2f',s) '_PVpl.wav'];
        name_HP = [name(1:end-4) '_' sprintf('%0.2f',s) '_HP.wav'];
        name_ELAST = [name(1:end-4) '_' sprintf('%0.2f',s) '_ELAST.wav'];
        
        % generate audio files
        % Original
        [x,fsAudio] = audioread([pathData name]);
        audiowrite([pathHtml name_ORIG],x,fsAudio);
        
        % OLA
        paramOLA.tolerance = 0;
        paramOLA.synHop = 128;
        paramOLA.win = win(256,2); % hann window
        yOLA = wsolaTSM(x,s,paramOLA);
        audiowrite([pathHtml name_OLA],yOLA,fsAudio);
        
        % WSOLA
        yWSOLA = wsolaTSM(x,s);
        audiowrite([pathHtml name_WSOLA],yWSOLA,fsAudio);
        
        % Phase Vocoder
        yPV = pvTSM(x,s);
        audiowrite([pathHtml name_PV],yPV,fsAudio);
        
        % Phase Vocoder with identity phase locking
        paramPVpl.phaseLocking = 1;
        yPVpl = pvTSM(x,s,paramPVpl);
        audiowrite([pathHtml name_PVpl],yPVpl,fsAudio);
        
        % TSM based on HPSS
        yHP = hpTSM(x,s);
        audiowrite([pathHtml name_HP],yHP,fsAudio);
        
        % elastique
        yELAST = elastiqueTSM(x,s);
        audiowrite([pathHtml name_ELAST],yELAST,fsAudio);
        
        
        % generate table entries
        % setup new table row
        fprintf(hTables, '<tr align="center">\n');
        fprintf(hTables, '<td align="left" class="name">%s</td>\n',...
            name(1:end-4));
        
        % Original
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_ORIG);
        
        % OLA
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_OLA);
        
        % WSOLA
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_WSOLA);
        
        % Phase Vocoder
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_PV);
        
        % Phase Vocoder with identity phase locking
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_PVpl);
        
        % TSM based on HPSS
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_HP);
        
        % elastique
        fprintf(hTables,'<td><a href="%s">[wav]</a></td>\n',name_ELAST);
        
        % close table row
        fprintf(hTables, '</tr>\n');     
        
    end
    
    % closing the table
    fprintf(hTables, '</table>\n');
    fprintf(hTables, '</center>\n');
    
end

fclose(hTables);


% load the written table
fid = fopen([pathHtml nameTable],'r');
table = fread(fid, '*char')';
fclose( fid );

% replace the labels in indexTemplate
index_template = regexprep( index_template, 'LABEL_TABLE', table);

% write the index.html
fprintf(index_out,'%s',index_template);
fclose(index_out);
 
% copy the stylesheet to the html folder
copyfile([pathData nameStyle],[pathHtml nameStyle]);