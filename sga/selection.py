#-------------------------------------------------------------------------------
# Author: Justin Lewis Salmon <mccrustin@gmail.com>
#-------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from bisect import bisect_left
import copy
import random


def roulette(population):
    """
    Return a new population list after performing roulette wheel selection.

    :param population:  the previous population
    :returns:           the newly selected population
    """
    cumulative_fitnesses = list()
    cumulative_fitnesses.append(population[0].fitness())

    #---------------------------------------------------------------------------
    # Record the cumulative fitness scores.  It doesn't matter whether the
    # population is sorted or not.  We will use these cumulative scores to work
    # out an index into the population.  The cumulative array itself is
    # implicitly sorted since each element must be greater than the previous
    # one.  The numerical difference between an element and the previous one is
    # directly proportional to the probability of the corresponding candidate in
    # the population being selected.
    #---------------------------------------------------------------------------
    for i in xrange(1, len(population)):
        fitness = population[i].fitness()
        cumulative_fitnesses.append(cumulative_fitnesses[i - 1] + fitness)

    selection = list()
    for i in xrange(0, len(population)):

        random_fitness = random.random() * cumulative_fitnesses[-1]
        index = bisect_left(cumulative_fitnesses, random_fitness)

        if index < 0:
            index = abs(index + 1)

        selection.append(population[index])

    return selection


def tournament(population):
    """
    Return a new population list after performing tournament selection

    :param population:  the previous population
    :returns:           the newly selected population
    """
    tournament_size = population.tournament_size \
        if population.tournament_size else 10
    selection       = list()

    while len(selection) < len(population):
        tournament_list = list()

        for _ in xrange(tournament_size):
            tournament_list.append(population
                                   [random.randint(0, len(population) - 1)])

        max_indiv = tournament_list[0]
        for i in xrange(tournament_size):
            if tournament_list[i].fitness() > max_indiv.fitness():
                max_indiv = tournament_list[i]

            elif tournament_list[i].fitness() == max_indiv.fitness():
                if len(tournament_list[i]) < len(max_indiv):
                    max_indiv = tournament_list[i]

        selection.append(max_indiv)

    return selection
