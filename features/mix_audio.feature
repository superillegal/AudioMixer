Feature: Mixing Audio Files

  Scenario: Mixing two audio files
    Given a new mixing session
    Given the audio file "audio1.wav"
    And the audio file "audio2.wav"
    When I mix "audio1.wav" from 0 seconds to 5 seconds
    And I mix "audio2.wav" from 2 seconds to 7 seconds into "mixed_audio.wav"
    Then the output file "mixed_audio.wav" should exist
    And the output file should not be empty