fft_values = fft(samples)

mean_value = mean(abs(fft))
threshold = 1.1*mean_value

fft_values[abs(fft_values) < threshold] = 0

filteredSample = ifft(fft_values)