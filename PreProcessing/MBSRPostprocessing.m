%To run this script, go to the EEG_Lab_Share directory on the desktop, 
%type MBSRPreprocessing1('/data/home/mbsr/Desktop/Processing_Scripts/MBSRsubids.txt'); into the MATLAB console and hit enter.
% unless you want to run the processing on a subset of the ids, then make a new textfile with the subset of ids you want to run on.



function MBSRPostprocessing(subidsdirectory)

	subidfile = fopen(subidsdirectory);
	columntypes = '%s';
	subidlist = textscan(subidfile, columntypes, 'Delimiter', '\t');

	baselinestart = -300;
	baselineend = 0;

%This runs a for loop over the subject ids and runs the processing functions, defined within this nested function
	for subindex = 1:length(subidlist{1}) ;
		subjectid = subidlist{1}{subindex};
	
		subjectdir = strcat('/data/home/mbsr/Desktop/PostData/', subjectid, '/');
	
		EEG = interpolatechannels(subjectid, subjectdir);
		EEG = rereference(EEG, subjectid, subjectdir);
		EEG = baselinecorrect(EEG, subjectid, subjectdir, baselinestart, baselineend);

	end 
end


function EEG = interpolatechannels(subjectid, subjectdir)
	% interpolates rejected channels modelling channel locations from
	% a full dataset (_1lowpass)
	EEG = pop_loadset('filename', strcat(num2str(subjectid), '_8icarej.set'), 'filepath', subjectdir);
	lowpass = strcat(num2str(subjectid), '_4epochs.set');
	fullchannelset = pop_loadset('filename', lowpass, 'filepath', subjectdir);
	EEG = pop_interp(EEG, fullchannelset.chanlocs, 'spherical');
	EEG.setname = strcat(num2str(subjectid), '_9chaninterpol')
	pop_saveset(EEG, 'filename', EEG.setname, 'filepath', subjectdir);
	EEG = eeg_checkset( EEG );
end

function EEG = rereference(EEG, subjectid, subjectdir)
	% rereferences data to average of channels and recomputes Cz
	EEG = pop_reref( EEG, []);
	EEG.setname = strcat(num2str(subjectid), '_10reref')
	pop_saveset(EEG, 'filename', EEG.setname, 'filepath', subjectdir);
	EEG = eeg_checkset( EEG );
end

function EEG = baselinecorrect(EEG, subjectid, subjectdir, baselinestart, baselineend);
	EEG = pop_rmbase(EEG, [baselinestart baselineend]);
	EEG = eeg_checkset(EEG);
	EEG.setname = strcat(num2str(subjectid), '_11baselinecorr')
	EEG.filename = EEG.setname
	pop_saveset(EEG, 'filename', EEG.setname, 'filepath', subjectdir);
	EEG = eeg_checkset(EEG);
end
