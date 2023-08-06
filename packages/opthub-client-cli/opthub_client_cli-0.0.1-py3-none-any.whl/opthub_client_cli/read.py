# coding: utf-8
"""
Low-level read commands.
"""
import logging

import click

from .util import AliasedGroup, execute, str_to_dict

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, name='list')
def read():
    """List objects."""


@read.command(help='List users on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def users(ctx, **kwargs):
    """List users on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.users(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: users_bool_exp = {}
        ) {
          users(limit: $limit, offset: $offset, where: $query) {
            name
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List problems on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def problems(ctx, **kwargs):
    """List problems on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.problems(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: problems_bool_exp = {}
        ) {
          problems(limit: $limit, offset: $offset, where: $query) {
            id
            name
            description
            image
            owner { name }
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List metrics on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def metrics(ctx, **kwargs):
    """List metrics on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.metrics(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: metrics_bool_exp = {}
        ) {
          metrics(offset: $offset, limit: $limit, where: $query) {
            id
            name
            description
            image
            owner { name }
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List competitions on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def competitions(ctx, **kwargs):
    """List competitions on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.competitions(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: competitions_bool_exp = {}
        ) {
          competitions(offset: $offset, limit: $limit, where: $query) {
            id
            name
            description
            owner { name }
            matches { id }
            open_at
            close_at
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List progresses on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def progresses(ctx, **kwargs):
    """List progresses on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.progresses(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: progresses_bool_exp = {}
        ) {
          progresses(offset: $offset, limit: $limit, where: $query) {
            user_id
            match_id
            budget
            submitted
            evaluating
            evaluated
            scoring
            scored
            scores
            created_at
            updated_at
            evaluation_started_at
            evaluation_finished_at
            scoring_started_at
            scoring_finished_at
          }
        }
        ''',
        kwargs)


@read.command(help='List matches on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def matches(ctx, **kwargs):
    """List matches on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.matches(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: matches_bool_exp = {}
        ) {
          matches(offset: $offset, limit: $limit, where: $query) {
            id
            competition_id
            problem_id
            metric_id
            budget
            environment
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@read.command(help='List solutions on OptHub.')
@click.option('-q', '--query', type=str, callback=str_to_dict,
              help='Search query.')
@click.option('-o', '--offset', type=click.IntRange(min=0),
              default=0, help='Offset.')
@click.option('-l', '--limit', type=click.IntRange(1, 100),
              default=50, help='Limit.')
@click.pass_context
def solutions(ctx, **kwargs):
    """List solutions on OptHub.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('list.solutions(%s)', kwargs)
    execute(
        ctx,
        '''
        query(
          $offset: Int!
          $limit: Int!
          $query: solutions_bool_exp = {}
        ) {
          solutions(offset: $offset, limit: $limit, where: $query) {
            id
            owner { name }
            match_id
            variable
            objective
            constraint
            score
            created_at
            updated_at
            evaluation_started_at
            evaluation_finished_at
            scoring_started_at
            scoring_finished_at
          }
        }
        ''',
        kwargs)
