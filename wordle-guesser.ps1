$global:guesses = ".\guesses.txt"
$global:answers = ".\answers.txt"

class WordleGuesser
{
    [array] $guesses
    [array] $answers

    [string] $guess
    [string] $pattern
    [string] $best_guess

    [bool] $running

    WordleGuesser()
    {
        $this.guesses         = $global:guesses
        $this.answers         = $global:answers
        $this.guess           = ""
        $this.pattern         = ""
        $this.best_guess      = "salet"
        $this.running         = $true
    }

    [void] start()
    {
        while ($this.running)
        {
            $this.guesser()
        }
    }

    [void] guesser()
    {
        $this.guess           = read-host "Guess"
        $this.pattern         = read-host "Pattern"

        if (-not $this.guess -or -not $this.pattern)
        {
            $this.running     = $false
            return
        }

        if ($this.guess -notin $this.guesses)
        {
            write-host $this.guess "is not guessable!"
            return
        }

        $this.checker()

        if (-not $this.answers)
        {
            $this.running     = $false
            return
        }

        $this.NextGuess()

        write-host $this.best_guess

        if ($this.answers.length -eq 1)
        {
            $this.running     = $false
            return
        }
    }

    [void] checker()
    {
        $good_letters         = @()

        for ($index = 0; $index -lt $this.guess.length; $index++)
        {
            $letter           = $this.guess[$index]

            if ($this.pattern[$index] -ne "b")
            {
               $good_letters += $letter
            }
        }
        
        for ($index = 0; $index -lt $this.guess.length; $index++)
        {
            $letter           = $this.guess[$index]

            if ($this.pattern[$index] -eq "g")
            {
                $this.answers = $this.answers | where { $_[$index] -eq $letter }
            }
            
            if ($this.pattern[$index] -eq "y")
            {
                $this.answers = $this.answers | where { ($_[$index] -ne $letter) -and ($_ -match $letter) }
            }

            if (($this.pattern[$index] -eq "b") -and ($letter -notin $good_letters))
            {
                $this.answers = $this.answers | where { $_ -notmatch $letter }
            }
        }

    }

    [void] nextguess()
    {
        if ($this.answers.length -lt 3)
        {
            $this.best_guess  = $this.answers[0]
            return
        }

        $best_word            = ""
        $best_entropy         = 0

        foreach ($guess in $this.guesses)
        {
            $entropy          = $this.entropy($guess)

            if ($entropy -gt $best_entropy)
            {
                $best_word    = $guess
                $best_entropy = $entropy
            }
        }
        
        $this.best_guess      = $best_word
    }

    [float] entropy($guess)
    {
        $patterns             = @{}

        foreach ($answer in $this.answers)
        {
            $local_pattern    = $this.getpattern($guess, $answer)

            if (-not $patterns.containskey($local_pattern))
            {
                $patterns[$local_pattern] = 0
            }
            
            $patterns[$local_pattern] += 1
        }

        $total_answers        = $this.answers.length

        $entropy = $this.calculateentropy($total_answers, $patterns)
        return $entropy
    }

    [string] getpattern($guess, $answer)
    {
        $local_pattern        = @("") * 5

        for ($index = 0; $index -lt $this.guess.length; $index++)
        {
            $letter           = $guess[$index]
            
            if ($letter -eq $answer[$index])
            {
                $local_pattern[$index] = "g"
            }

            elseif (($letter -ne $answer[$index]) -and ($answer -match $letter))
            {
                $local_pattern[$index] = "y"
            }

            elseif ($answer -notmatch $letter)
            {
                $local_pattern[$index] = "b"
            }
        }

        $local_pattern        = $local_pattern -join ""
        return $local_pattern
    }

    [float] calculateentropy($total_answers, $patterns)
    {
        $entropies            = @()

        foreach ($pattern in $patterns.getenumerator())
        {
            $count            = $pattern.value
            $probability      = $count / $total_answers
            $entropy_amount   = [math]::log(1 / $probability) / [math]::log(2)

            for ($index = 0; $index -lt $count; $index++)
            {
                $entropies   += $entropy_amount
            }
        }

        $entropy_measured     = $entropies | measure -sum
        $entropy              = $entropy_measured.sum / $entropy_measured.count

        return $entropy
    }
}

function Wordle-Guesser {
    $wordle_guesser = [WordleGuesser]::new()
    $wordle_guesser.start()
}
