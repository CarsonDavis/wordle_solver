from django.shortcuts import render

from .forms import GameForm
from .utils.game_mechanics import Game


def get_guess(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            game = Game()
            game_state = [
                [
                    (request.POST['first'], request.POST['first_results']),
                    (request.POST['second'], request.POST['second_results']),
                    (request.POST['third'], request.POST['third_results']),
                    (request.POST['fourth'], request.POST['fourth_results']),
                    (request.POST['fifth'], request.POST['fifth_results']),
                ],
                # [
                #     ("r", "position"),
                #     ("e", "position"),
                #     ("s", "wrong"),
                #     ("i", "position"),
                #     ("n", "position"),
                # ],
            ]
            for turn in game_state:
                game.update_position_data(turn)
            game.update_possible_words()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')
            return render(
                request, 'guess.html', {'form': form, 'possible_words': game.possible_words}
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'guess.html', {'form': form})
