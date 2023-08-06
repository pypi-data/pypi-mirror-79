# coding: utf-8
"""
Low-level delete commands.
"""
import logging

import click

from .util import AliasedGroup, StrLength, execute

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup)
def delete():
    """Delete an object."""


@delete.command(help='Delete a problem.')
@click.argument('id', type=StrLength(min=2))
@click.pass_context
def problem(ctx, **kwargs):
    """Delete a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('delete.problem(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation delete_problem($id: String!) {
          delete_problems_by_pk(id: $id) {
            id
            name
            description
            image
            owner {name}
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete a metric.')
@click.argument('id', type=StrLength(min=2))
@click.pass_context
def metric(ctx, **kwargs):
    """Delete a metric.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('delete.metric(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: String!) {
          delete_metrics_by_pk(id: $id) {
            id
            name
            description
            image
            owner {name}
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete a match.')
@click.argument('id', type=int)
@click.pass_context
def match(ctx, **kwargs):
    """Delete a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('delete.match(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: Int!) {
          delete_matches_by_pk(id: $id) {
            id
            competition_id
            problem_id
            metric_id
            environment
            budget
            created_at
            updated_at
          }
        }
        ''',
        kwargs)


@delete.command(help='Delete a competition.')
@click.argument('id', type=StrLength(min=2))
@click.pass_context
def competition(ctx, **kwargs):
    """Delete a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('delete.competition(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation($id: String!) {
          delete_competitions_by_pk(id: $id) {
            id
            name
            description
            owner {name}
            open_at
            close_at
            created_at
            updated_at
          }
        }
        ''',
        kwargs)
