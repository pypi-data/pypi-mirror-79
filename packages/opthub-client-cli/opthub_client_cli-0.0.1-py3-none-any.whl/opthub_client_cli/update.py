# coding: utf-8
"""
Low-level update commands.
"""
import logging

import click

from .util import AliasedGroup, StrLength, execute

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, help='Update an object.')
def update():
    """Update an object."""


@update.command(help='Update a problem.')
@click.argument('id-to-update', type=StrLength(min=2))
@click.option('-i', '--id',
              type=StrLength(min=2),
              help='New ID.')
@click.option('-n', '--name',
              type=StrLength(min=1),
              help='New name.')
@click.option('-d', '--description',
              type=StrLength(min=1),
              help='New description.')
@click.option('-t', '--image',
              type=StrLength(min=1),
              help='New Docker image tag.')
@click.pass_context
def problem(ctx, **kwargs):
    """Update a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('update.problem(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: String!
          $id: String!
          $name: String!
          $description: String!
          $image: String!
        ) {
          update_problems_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              id: $id
              name: $name
              description: $description
              image: $image
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update a metric.')
@click.argument('id-to-update', type=StrLength(min=2))
@click.option('-i', '--id',
              type=StrLength(min=2),
              help='New ID.')
@click.option('-n', '--name',
              type=StrLength(min=1),
              help='New name.')
@click.option('-d', '--description',
              type=StrLength(min=1),
              help='New description.')
@click.option('-t', '--image',
              type=StrLength(min=1),
              help='New Docker image tag.')
@click.pass_context
def metric(ctx, **kwargs):
    """Update a metric.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('update.metric(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: String!
          $id: String!
          $name: String!
          $description: String!
          $image: String!
        ) {
          update_metrics_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              id: $id
              name: $name
              description: $description
              image: $image
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update a match.')
@click.argument('id-to-update', type=int)
@click.option('-c', '--competition',
              type=StrLength(min=2),
              help='New competition ID.')
@click.option('-p', '--problem',
              type=StrLength(min=2),
              help='New problem ID.')
@click.option('-m', '--metric',
              type=StrLength(min=2),
              help='New metric ID.')
@click.option('-e', '--environment',
              type=str,
              help='New environment variables.')
@click.option('-b', '--budget',
              type=click.IntRange(min=1),
              help='New budget.')
@click.pass_context
def match(ctx, **kwargs):
    """Update a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('update.match(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: Int!
          $competition: String!
          $problem: String!
          $metric: String!
          $environment: String!
          $budget: Int!
        ) {
          update_matches_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              competition_id: $competition
              problem_id: $problem
              metric_id: $metric
              environment: $environment
              budget: $budget
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)


@update.command(help='Update a competition.')
@click.argument('id-to-update', type=StrLength(min=2))
@click.option('-i', '--id',
              type=StrLength(min=2),
              help='New ID.')
@click.option('-n', '--name',
              type=StrLength(min=1),
              help='New name.')
@click.option('-d', '--description',
              type=StrLength(min=1),
              help='New description.')
@click.option('-o', '--open-at',
              type=click.DateTime(),
              help='New open date.')
@click.option('-c', '--close-at',
              type=click.DateTime(),
              help='New close date.')
@click.pass_context
def competition(ctx, **kwargs):
    """Update a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('update.competition(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id_to_update: String!
          $id: String!
          $name: String!
          $description: String!
          $open_at: String!
          $close_at: String!
        ) {
          update_competitions_by_pk(
            pk_columns: { id: $id_to_update }
            _set: {
              id: $id
              name: $name
              description: $description
              open_at: $open_at
              close_at: $close_at
            }
          ) {
            id
            updated_at
          }
        }
        ''',
        kwargs)
