using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;


/* 
 * This script is meant to handle the audio throughout the game as well as sfx. 
 * 
 * Yes I do comment this much, shut up (>_<)
 * 
 * I used this guy for reference
 * https://www.youtube.com/watch?v=2ldKKV1h5Ww
 * 
 */



public class AudioManager : MonoBehaviour
{

    //Holds the looped dictionary
    private Dictionary<SoundType, AudioSource> loopingSources = new Dictionary<SoundType, AudioSource>();


    //SFX Types (Just add more as you need)
    public enum SoundType
    {
        walkDefault,
        walkGrass,
        walkGravel,
        walkConcrete,
        door,
        generator,
    }

    
    //Adds the SoundType as a selectable thing in the
    //inspector to quickly assign SFX.
    [System.Serializable]
    public class Sound
    {
        public SoundType soundType;
        public AudioClip soundClip;

        [Range(0f, 1f)]
        public float volume = 1f;

        [HideInInspector]
        public AudioSource source;
    }

    //Makes the AudioManager a Singleton which prevents other
    //scripts from making duplicate managers when calling it. 
    public static AudioManager audioManagerInstance;


    //Add the different sound effects - found in the inspector
    public Sound[] allSounds;

    //Used to track queued sound effects
    private Dictionary<SoundType, Sound> soundDictionary = new Dictionary<SoundType, Sound>();
    private AudioSource musicSource;



    private void Awake()
    {
        //Assign singlton
        audioManagerInstance = this;

        foreach(var s in allSounds)
        {
            soundDictionary[s.soundType] = s;
        }
    }


    public void Play(SoundType type)
    {
        //Make sure there's a sound assigned to the type
        if (!soundDictionary.TryGetValue(type, out Sound s))
        {
            Debug.LogWarning($"Sound type: {type} not found!");
            return;
        }

        //Creates a new sound object
        var soundObject = new GameObject($"Sound_{type}");
        var audioSource = soundObject.AddComponent<AudioSource>();

        //Assigns the sound properties
        audioSource.clip = s.soundClip;
        audioSource.volume = s.volume;

        //Plays the sound
        audioSource.Play();

        //Destorys the object when the clip is done playing
        Destroy(soundObject, s.soundClip.length);
    }


    //Handles the sounds that are meant to loop
    public void StartLoop(SoundType type, bool walk = false)
    {
        //Make sure there's a sound assigned to the type
        if (!soundDictionary.TryGetValue(type, out Sound s))
        {
            Debug.LogWarning($"Sound type: {type} not found!");
            return;
        }

        // If already playing, do nothing
        if (loopingSources.ContainsKey(type) && loopingSources[type].isPlaying) 
        { 
            return;
        }


        AudioSource source;
        if (!loopingSources.ContainsKey(type))
        {
            // First shitty loop:
            // Look, I know it is ugly, but it gets the job done for now, if we are hurting for performance
            // it can be replaced, but until then, shitty soudloop go!!! There is a second one below this one
            if (walk == true)
            {
                StopLoop(SoundType.walkDefault);
                StopLoop(SoundType.walkGrass);
                StopLoop(SoundType.walkConcrete);
                StopLoop(SoundType.walkGravel);
            }
            var soundObject = new GameObject($"Loop_{type}");
            source = soundObject.AddComponent<AudioSource>();

            source.clip = s.soundClip;
            source.volume = s.volume;


            source.loop = true;
            loopingSources[type] = source;
        }
        else
        {
            // Here is the other shitty loop, see comment above about the first shitty loop
            if (walk == true)
            {
                StopLoop(SoundType.walkDefault);
                StopLoop(SoundType.walkGrass);
                StopLoop(SoundType.walkConcrete);
                StopLoop(SoundType.walkGravel);
            }
            source = loopingSources[type];
        }

        source.Play();
}

    // Stops the sound loops
    public void StopLoop(SoundType type)
    {
        if (loopingSources.ContainsKey(type) && loopingSources[type].isPlaying)
        {
            loopingSources[type].Stop();
        }
    }




    //Controls the music tracks that play
    public void ChangeMusic(SoundType type)
    {
        if (!soundDictionary.TryGetValue(type, out Sound track))
        {
            Debug.LogWarning($"Music track {type} not found!");
            return;
        }

        if (musicSource == null)
        {
            var container = new GameObject("SoundTrackObj");
            musicSource = container.AddComponent<AudioSource>();
            musicSource.loop = true;
        }

        musicSource.clip = track.soundClip;
        musicSource.Play();
    }
}
