# coding: utf-8
"""
Low-level create commands.
"""
import logging

import click

from .util import AliasedGroup, StrLength, execute

_logger = logging.getLogger(__name__)


@click.group(cls=AliasedGroup, help='Create an object.')
def create():
    """Create an object."""


@create.command(help='Create a problem.')
@click.option('-i', '--id',
              type=StrLength(min=2), prompt=True,
              help='ID.')
@click.option('-n', '--name',
              type=StrLength(min=1), prompt=True,
              help='Name.')
@click.option('-d', '--description',
              type=StrLength(min=1), prompt=True,
              help='Description.')
@click.option('-t', '--image',
              type=StrLength(min=1), prompt=True,
              help='Docker image tag.')
@click.pass_context
def problem(ctx, **kwargs):
    """Create a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('create.problem(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id: String!
          $name: String!
          $description: String!
          $image: String!
        ) {
          insert_problems_one(
            object: {
              id: $id
              name: $name
              description: $description
              image: $image
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create a metric.')
@click.option('-i', '--id',
              type=StrLength(min=2), prompt=True,
              help='ID.')
@click.option('-n', '--name',
              type=StrLength(min=1), prompt=True,
              help='Name.')
@click.option('-d', '--description',
              type=StrLength(min=1), prompt=True,
              help='Description.')
@click.option('-t', '--image',
              type=StrLength(min=1), prompt=True,
              help='Docker image tag.')
@click.pass_context
def metric(ctx, **kwargs):
    """Create a metric.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('create.metric(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id: String!
          $name: String!
          $description: String!
          $image: String!
        ) {
          insert_metrics_one(
            object: {
              id: $id
              name: $name
              description: $description
              image: $image
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create a match.')
@click.option('-c', '--competition',
              type=StrLength(min=2), required=True, prompt=True,
              help='Competition ID.')
@click.option('-p', '--problem',
              type=StrLength(min=2), required=True, prompt=True,
              help='Problem ID.')
@click.option('-m', '--metric',
              type=StrLength(min=2), required=True, prompt=True,
              help='Metric ID.')
@click.option('-e', '--environment', prompt=True,
              type=str,
              help='Environment variables.')
@click.option('-b', '--budget',
              type=click.IntRange(min=1), required=True, prompt=True,
              help='Budget.')
@click.pass_context
def match(ctx, **kwargs):
    """Create a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('create.match(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $competition: String!
          $problem: String!
          $metric: Int!
          $environment: String!
          $budget: Int!
        ) {
          insert_matches_one(
            object: {
              competition_id: $competition
              problem_id: $problem
              metric_id: $metric
              environment: $environment
              budget: $budget
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)


@create.command(help='Create a competition.')
@click.option('-i', '--id', type=StrLength(min=2), required=True,
              prompt=True, help='ID.')
@click.option('-n', '--name', type=StrLength(min=1), required=True,
              prompt=True, help='Name.')
@click.option('-d', '--description', type=StrLength(min=1), required=True,
              prompt=True, help='Description.')
@click.option('-o', '--open-at', type=click.DateTime(), required=True,
              prompt=True, help='Open date.')
@click.option('-c', '--close-at', type=click.DateTime(), required=True,
              prompt=True, help='Close date.')
@click.pass_context
def competition(ctx, **kwargs):
    """Create a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.info('create.competition(%s)', kwargs)
    execute(
        ctx,
        '''
        mutation(
          $id: String!
          $name: String!
          $description: String!
          $open_at: String!
          $close_at: String!
        ) {
          insert_competitions_one(
            object: {
              id: $id
              name: $name
              description: $description
              open_at: $open_at
              close_at: $close_at
            }
          ) {
            id
            created_at
          }
        }
        ''',
        kwargs)
