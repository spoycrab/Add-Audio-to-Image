import argparse
import subprocess
import re
import os

def getAudioDuration(musica):
    """
    musica: Audio file path
    """
    comando_ffmpeg = ['ffmpeg', '-i', musica]
    
    # Executar o comando ffmpeg e capturar a saída
    resultado = subprocess.run(comando_ffmpeg, stderr=subprocess.PIPE, text=True)
    
    # Procurar pela linha que contém informações sobre a duração
    duracao_linha = re.search(r'Duration: (\d+:\d+:\d+\.\d+)', resultado.stderr)
    
    if duracao_linha:
        audioDuration = duracao_linha.group(1)
        return audioDuration
    else:
        return None 

def imageWithMusic(input_files):
    if len(input_files) != 2:
        print("Select only 2 files")
        return
    #Lista de extenções de audio e imagem
    audio_extension_list = [".mp3", ".wav", ".ogg", ".flac", ".aac"]
    image_extension_list = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg"]

    for input_file in input_files:
        print(f"Files: {input_file}")
        nome, extensao = os.path.splitext(input_file) #Pega o tipo de extenção
        if extensao in audio_extension_list:
            music = input_file
        if extensao in image_extension_list:
            image = input_file
            tipoImage = extensao

    if image is None or music is None:
        print("No audio or image found")
        return
    
    print(f"Imagem: {image}")
    print(f"Musica: {music}")

    audioDuration = getAudioDuration(music)

    filePath = os.path.dirname(input_files[0])
    if tipoImage == ".gif":
        os.system(f"ffmpeg -i \"{image}\" -i \"{music}\" -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" -c:v libx264 -tune stillimage -c:a aac -strict experimental -b:a 192k -pix_fmt yuv420p -shortest {filePath}/video_music.mp4")
    else:
        os.system(f"ffmpeg -loop 1 -i \"{image}\" -i \"{music}\" -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" -c:v libx264 -tune stillimage -c:a aac -strict experimental -b:a 192k -pix_fmt yuv420p -shortest {filePath}/video_music.mp4")
        
    os.system(f"ffmpeg -i {filePath}/video_music.mp4 -ss 0 -to {audioDuration} {filePath}/image_with_music.mp4")
    os.remove(f"{filePath}/video_music.mp4")
    print(filePath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs='+')
    args = parser.parse_args()
    try:
        imageWithMusic(args.input_files)
    except Exception as e:
        print(e)
        input()
    input()