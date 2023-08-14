cmake_minimum_required(VERSION 3.13)

# include_directories(${CMAKE_CURRENT_SOURCE_DIR})

file(GLOB_RECURSE audacity_files ${CMAKE_CURRENT_SOURCE_DIR}/*.aup)

set(audio_asm ${CMAKE_CURRENT_SOURCE_DIR}/src/sounds.S)
set(python_script ${CMAKE_CURRENT_SOURCE_DIR}/wav2bin.py)
file(WRITE ${audio_asm} "")

foreach(audacity_file ${audacity_files})
  cmake_path(GET audacity_file STEM filename)
  set(bin_file ${CMAKE_CURRENT_SOURCE_DIR}/bin/${filename}.bin)
  set(wav_file ${CMAKE_CURRENT_SOURCE_DIR}/${filename}/${filename}.wav)
  add_custom_command(
    OUTPUT ${bin_file}
    COMMAND python ${python_script} ${wav_file} ${bin_file}
    MAIN_DEPENDENCY ${wav_file}
    DEPENDS ${python_script})
  add_custom_target(${filename}
    DEPENDS ${bin_file})
  list(APPEND audio_depends ${filename})
  file(APPEND ${audio_asm}
".global ${filename}_start
.global ${filename}_end
${filename}_start:
.incbin \"${bin_file}\"
${filename}_end:
")
endforeach()

set(SOUND_ASM ${audio_asm} PARENT_SCOPE)
set(SOUND_DEPENDS ${audio_depends} PARENT_SCOPE)
