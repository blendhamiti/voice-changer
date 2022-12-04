function y = convolution()
    args = argv();
  
    voice_file = args{1};
    env_file = args{2};

    [voice, fs] = audioread(voice_file);
    [env, env_fs] = audioread(env_file);

    voice1 = transpose(voice)(1,:);
    env1 = transpose(env)(1,:);

    pkg load signal;

    [P,Q] = rat(fs/env_fs);
    env1_resampled = resample(env1,P,Q);

    w = conv(voice1, env1_resampled);
    
    audiowrite('output.wav', w, fs);
end